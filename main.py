import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Ciao!', ['Buongiorno', 'Buonasera', 'hey', 'Salve', 'Ciao'], single_response=True)
    response('Grazie!', ['ciao', 'arrivederci'], single_response=True)
    response('Come posso aiutarti?', ['hai', 'bisogno', 'di', 'aiuto?'], required_words=['hai'])
    response('Grazie per metterti in conttato', ['grazie', 'prego'], single_response=True)
    response('A te!', ['Voglio', 'parlare', 'con', 'un', 'consulente'], required_words=['parlare', 'consulente'])

    # Longer responses
    response(long.R_B, ['voglio', 'consulenza'], required_words=['consulenza'])
    response(long.R_C, ['come', 'ti', 'aiuto?'], required_words=['come', 'aiuto'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('Tu: ')))