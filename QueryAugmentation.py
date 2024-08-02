
# this is the function for the query augmentation that the user input before sending it to the model
keywords = ["gun", "violence", "drugs", "crime", "abuse", "illegal", "addiction", "theft", "corruption",
            "harassment", "fraud", "assault", "trafficking", "murder", "scam", "exploitation",
            "terrorism", "suicide"]


def keyword_check(user_input):
    for keyword in keywords:
        if keyword in user_input:
            return 'invalid'
    return user_input


def query_augmentation(user_input):
    return keyword_check(user_input)
