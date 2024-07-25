import re
# this is the function for the query augmentation of the response received from the model
def response_augmentation(response):
    good_keywords = ["data", "sql", "management", "report", "dashboard", "support", "ketchup", "clinic", "quality"]
    bad_keywords = ["gun", "violence", "drugs"]

    if any(keyword in response for keyword in good_keywords):
        print("response seems valid")
    elif any(keyword in response for keyword in bad_keywords):
        print("response invalid")
    else:
        print("can't determine the quality")

    return response


# Example usage:
response = "This is a sample response containing good2."
response_augmentation(response)


def transform_to_html(text):
    # Handle SQL code snippets first
    def replace_sql(match):
        code_content = match.group(1).replace('*', '&#42;')
        return f'<code>{code_content}</code>'

    text = re.sub(r'```(.*?)```', replace_sql, text, flags=re.DOTALL)

    # Replace markdown formatting with HTML tags
    html_text = text.replace('\n\n', '</p><p>')
    html_text = html_text.replace('\n* ', '<li>')
    html_text = html_text.replace('</p><p><li>', '</p><ul><li>')
    html_text = html_text.replace('</li><p>', '</li></ul><p>')
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html_text)
    html_text = html_text.replace('* ', '<li>')
    html_text = html_text.replace('\n', '<br>')

    # Wrap the entire text in a <div> tag
    html_text = f'<div><p>{html_text}</p></div>'

    return html_text
