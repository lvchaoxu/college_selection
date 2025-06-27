import pandas as pd


def extract_college(name: str) -> dict[str, str]:
    """
    解析专业名称
    """
    city_name = ""
    college_category = ""
    if name.find("(") != -1:
        college_name = name[:name.find("(")]
    else:
        college_name = name[: name.find("[")]
    if name.find("(") != -1 and name.find(")") != -1:
        city_name = name[name.find("(") + 1: name.find(")")]
    if name.find("[") != -1 and name.find("]") != -1:
        college_category = name[name.find("[") + 1: name.rfind("]")]
    return {
        "college_name": college_name,
        "city_name": city_name,
        "college_category": college_category
    }


def extract_major(major_name: str) -> dict[str, str]:
    if major_name.find("(") != -1:
        major = major_name[:major_name.find("(")]
        major_comment = major_name[major_name.find("(") + 1: -1]
    else:
        major = major_name
        major_comment = ""
    return {
        "major_name": major,
        "major_comment": major_comment
    }


if __name__ == "__main__":
    df = pd.read_excel("./20240722163024_933.xlsx",
                       header=None,
                       usecols="A:E",
                       skiprows=5,
                       nrows=18281,
                       names=["院校代号", "院校名称", "专业代号", "专业名称", "投档最低分"],
                       dtype={"院校代号": "Int64",
                              "投档最低分": "Int64",
                              "专业代号": "string",
                              "院校名称": "string",
                              "专业名称": "string"})
    df['college_dict'] = df['院校名称'].apply(extract_college)
    df['院校名'] = df['college_dict'].apply(lambda x: x['college_name'])
    df['城市名'] = df['college_dict'].apply(lambda x: x['city_name'])
    df['院校类别'] = df['college_dict'].apply(lambda x: x['college_category'])
    df['major_dict'] = df['专业名称'].apply(extract_major)
    df['专业'] = df['major_dict'].apply(lambda x: x['major_name'])
    df['专业注释'] = df['major_dict'].apply(lambda x: x['major_comment'])
    df.drop(columns=['college_dict', 'major_dict', '院校名称', '专业名称'], axis=1, inplace=True)
    df.to_excel("./24年院校专业投档线.xlsx", index=False)
