import re
# this is the function for the query augmentation of the response received from the model
def response_augmentation(response):
    # response = ...
    return response


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
