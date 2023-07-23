from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import Extra

from langchain.callbacks.manager import AsyncCallbackManagerForChainRun, CallbackManagerForChainRun
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.prompts.base import BasePromptTemplate
from langchain.chains.base import Chain
from langchain.llms.base import LLM

from core.prompt import (
    information_extraction_raw_prompt,
    intent_recognition_raw_prompt,
    entity_recognition_raw_prompt,
    relevance_scoring_raw_prompt,
    answer_generation_raw_prompt,
)
from core.tool import jina_retriever


class MyCustomChain(Chain):
    """An example of a custom chain."""
    prompts_list: List[BasePromptTemplate] = [
        intent_recognition_raw_prompt(),
        entity_recognition_raw_prompt(),
        information_extraction_raw_prompt(),
        relevance_scoring_raw_prompt(),
        answer_generation_raw_prompt(),
    ]

    """Prompt object to use."""
    llm: Any
    output_key: str = "text"  # :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return self.prompts_list[0].input_variables

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    def _call(
        self,
        inputs:  Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        show_prompt = False
        run_manager = run_manager if run_manager else StdOutCallbackHandler()
        history = ""
        intent = ""
        entity = ""
        key_information = ""
        extra_information = ""

        # -> No.1 chain block: intent recognition
        def intent_recognition():
            run_manager.on_text("\nEntering intent recognition...\n")
            prompt_value = self.prompts_list[0].format_prompt(**inputs)

            if show_prompt:
                print("\nintent_recognition prompt:")
                print(prompt_value.text)

            response = self.llm.generate_prompt(
                [prompt_value], callbacks=run_manager.get_child(
                ) if run_manager else None
            )
            generated_text = response.generations[0][0].text

            run_manager.on_text(
                "intent_recognition respond: {}\n".format(generated_text))
            return generated_text

        # -> No.2 chain block: entity recognition
        def entity_recognition():
            run_manager.on_text("\nEntering entity recognition...\n")
            prompt_value = self.prompts_list[1].format_prompt(**inputs)

            if show_prompt:
                print("\nentity_recognition prompt:")
                print(prompt_value.text)

            response = self.llm.generate_prompt(
                [prompt_value], callbacks=run_manager.get_child(
                ) if run_manager else None
            )
            generated_text = response.generations[0][0].text

            run_manager.on_text(
                "entity_recognition respond: {}\n".format(generated_text))
            return generated_text

        # -> No.3 chain block: information extraction
        def information_extraction():
            run_manager.on_text("\nEntering information extraction...\n")
            prompt_value = self.prompts_list[2].format_prompt(**inputs)

            if show_prompt:
                print("\ninformation_extraction prompt:")
                print(prompt_value.text)

            response = self.llm.generate_prompt(
                [prompt_value], callbacks=run_manager.get_child(
                ) if run_manager else None
            )
            generated_text = response.generations[0][0].text

            run_manager.on_text(
                "information_extraction respond: {}\n".format(generated_text))
            return generated_text

        # -> No.4 chain block: relevance  scoring
        def relevance_scoring(extra_information: str):
            run_manager.on_text("\nEntering relevance  scoring...\n")
            prompt_value = self.prompts_list[3].format_prompt(
                query=inputs['query'], extra_information=extra_information)

            if show_prompt:
                print("\nrelevance_scoring prompt:")
                print(prompt_value.text)

            response = self.llm.generate_prompt(
                [prompt_value], callbacks=run_manager.get_child(
                ) if run_manager else None
            )
            generated_text = response.generations[0][0].text

            run_manager.on_text(
                "relevance_scoring respond: {}\n".format(generated_text))
            return generated_text

        # -> No.5 chain block: answer  generation
        def answer_generation(history: str, intent: str, entity: str, key_information: str, extra_information: str):
            run_manager.on_text("\nEntering answer  generation...\n")
            prompt_value = self.prompts_list[4].format_prompt(
                query=inputs['query'],
                history=history,
                intent=intent,
                entity=entity,
                key_information=key_information,
                extra_information=extra_information)

            if show_prompt:
                print("\nanswer_generation prompt:")
                print(prompt_value.text)

            response = self.llm.generate_prompt(
                [prompt_value], callbacks=run_manager.get_child(
                ) if run_manager else None
            )
            generated_text = response.generations[0][0].text

            run_manager.on_text(
                "answer_generation respond: {}\n".format(generated_text))
            return generated_text

        print(f"{inputs}")
        intent = intent_recognition()

        if intent not in ["闲聊", "物流"]:
            return {self.output_key: "你的问题不在我们的工作职责内"}

        entity = entity_recognition()
        key_information = information_extraction()

        docs = jina_retriever.run(tool_input={"query": key_information})

        rs = []
        for i, _ in enumerate(docs):
            content = docs[i].page_content
            print(f"\n额外信息[{i}]: ", content)
            r = relevance_scoring(extra_information=content)
            rs.append(r)
            if r == "是":
                extra_information += f"{i+1}.({content}), "
        # print(rs)

        generated_text = answer_generation(
            history, intent, entity, key_information, extra_information)

        return {self.output_key: ""}

        # return {self.output_key: generated_text}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # Your custom chain logic goes here
        # This is just an example that mimics LLMChain
        prompt_value = self.prompt.format_prompt(**inputs)

        # Whenever you call a language model, or another chain, you should pass
        # a callback manager to it. This allows the inner run to be tracked by
        # any callbacks that are registered on the outer run.
        # You can always obtain a callback manager for this by calling
        # `run_manager.get_child()` as shown below.
        response = await self.llm.agenerate_prompt(
            [prompt_value], callbacks=run_manager.get_child() if run_manager else None
        )

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            await run_manager.on_text("Log something about this run")

        return {self.output_key: response.generations[0][0].text}

    @property
    def _chain_type(self) -> str:
        return "shadow_motion"
