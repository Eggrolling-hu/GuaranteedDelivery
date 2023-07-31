def read_qa_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()

    qa_list = []
    question, answer = None, None
    for line in lines:
        line = line.strip()  # remove leading/trailing whitespaces
        if line.startswith("问："):
            # save the previous qa pair if it exists
            if question and answer:
                qa_list.append(f"{question} {answer}")
            # start a new qa pair
            question = line
            answer = None
        elif line.startswith("答："):
            answer = line
    # don't forget the last qa pair
    if question and answer:
        qa_list.append(f"{question} {answer}")

    return qa_list


if __name__ == "__main__":
    print(read_qa_file("QA.txt"))
