
# this is the function for the query augmentation that the user input before sending it to the model
keywords = ['gun', 'terrorism', 'suicide']


def keyword_check(user_input):
    for keyword in keywords:
        if keyword in user_input:
            return 'invalid'
    return user_input

def modelCheck(user_input):
    # call AI model here
    return user_input


def query_augmentation(user_input):
    keywordCheckResult = keyword_check(user_input)
    if keywordCheckResult == 'invalid':
        result = modelCheck(user_input)
    else:
        result = keywordCheckResult
    return result


user_input_test = 'I like shotguns.'
test = query_augmentation(user_input_test)

print(test)
