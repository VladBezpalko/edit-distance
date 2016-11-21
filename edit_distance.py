"""
Edit distance calculator

This script calculates edit distance between two sequences
and show table of operations
"""
from terminaltables import AsciiTable

REPLACE = 'R'
INSERT = 'I'
DELETE = 'D'
MATCH = 'M'

COST_MAP = {
    REPLACE: 4,
    INSERT: 3,
    DELETE: 2,
    MATCH: 0,
}

NAME_MAP = {
    REPLACE: 'Replace',
    INSERT: 'Insert',
    DELETE: 'Delete',
    MATCH: 'Match',
}


def get_matrix(original, final):
    """
    Returns matrix with available edit prescriptions
    :param original: source string
    :param final: string which will be transformed
    :return: matrix with available edit prescriptions
    """
    size_origin, size_final = len(original) + 1, len(final) + 1
    matrix = list(map(list, [[0] * size_final] * size_origin))
    action_matrix = list(map(list, [[''] * size_final] * size_origin))

    for i in range(size_origin):
        matrix[i][0] = i
        action_matrix[i][0] = DELETE

    for j in range(size_final):
        matrix[0][j] = j
        action_matrix[0][j] = INSERT

    for i, char_origin in enumerate(original, 1):
        for j, char_final in enumerate(final, 1):
            replace_action = (REPLACE, MATCH)[char_origin == char_final]
            insert = matrix[i][j - 1] + COST_MAP[INSERT]
            delete = matrix[i - 1][j] + COST_MAP[DELETE]
            replace = matrix[i - 1][j - 1] + COST_MAP[replace_action]
            optimal = min(insert, delete, replace)
            matrix[i][j] = optimal

            if optimal == insert:
                action_matrix[i][j] = INSERT
            elif optimal == delete:
                action_matrix[i][j] = DELETE
            elif optimal == replace:
                action_matrix[i][j] = replace_action
    return action_matrix


def get_prescription(action_matrix):
    """
    Fetches most optimal and low by cost edit prescription
    :param action_matrix: available prescriptions
    :return: reversed prescription
    """
    i, j = len(action_matrix) - 1, len(action_matrix[0]) - 1
    prescr = []

    while i or j:
        action = action_matrix[i][j]
        prescr.append(action)
        if action == DELETE:
            i -= 1
        elif action == INSERT:
            j -= 1
        elif action in (REPLACE, MATCH):
            i -= 1
            j -= 1
        else:
            raise RuntimeError('Unknown action: %s', action)
    prescr.reverse()
    return prescr


def get_redaction(prescription, original, final):
    """
    Performs transformations
    :param prescription: reversed prescription
    :param original: source string
    :param final: string which will be transformed
    """
    total, i = 0, 0
    result = list(original)

    for action in prescription:
        if action == DELETE:
            result.pop(i)
        elif action == INSERT:
            result.insert(i, final[i])
            i += 1
        elif action == MATCH:
            i += 1
        elif action == REPLACE:
            result[i] = final[i]
            i += 1
        else:
            raise RuntimeError('Unknown action: %s', action)

        total += COST_MAP[action]

        yield action, i, total, result


def show_table(prescript, original, final):
    """
    Draws cute table with results
    """
    data = [
        ['Operation', 'z', 'Cost', 'Total'],
        ['Initial string', original, 0, 0]
    ]

    for action, i, total, result in get_redaction(prescript, original, final):
        temp_result = result[:]

        if action != DELETE:
            temp_result.insert(i - 1, '\033[4m')
            temp_result.insert(i + 1, '\033[0m')

        data.append(
            [
                NAME_MAP[action],
                ''.join(temp_result),
                COST_MAP[action], total
            ]
        )

    print(AsciiTable(data).table)


def main():
    """
    Main function
    """
    original = input('Enter first word: ')
    final = input('Enter second word: ')

    if not original:
        original = 'electrical engineering'

    if not final:
        final = 'computer science'

    prescription = get_prescription(get_matrix(original, final))

    show_table(prescription, original, final)


if __name__ == '__main__':
    main()
