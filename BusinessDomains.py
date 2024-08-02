business_domains = ['sales', 'finance', 'human resources', 'it']


def business_domain_check(user_input):
    for keyword in business_domains:
        if keyword in user_input:
            return keyword
    return 'no keyword'


def get_business_domain(user_input):
    selected_business_domain = business_domain_check(user_input)

    if selected_business_domain == 'no keyword':
        return 'no domain'
    else:
        return selected_business_domain
