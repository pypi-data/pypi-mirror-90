import math


def calculate_benford_stats(numerical_data):
    first_digit_index = 0
    first_digits = list(map(lambda number: int(str(number)[first_digit_index]), numerical_data))

    total_count = 0
    empirical_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ratios = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, 10):
        count_for_this_digit = first_digits.count(i)
        empirical_counts[i - 1] = count_for_this_digit
        total_count += count_for_this_digit

    if total_count > 0:
        for i in range(1, 10):
            ratios[i - 1] = empirical_counts[i - 1] / total_count

    return empirical_counts, ratios, total_count


def ascii_art_bar_graph(ratios, max_width):

    max_value = max(ratios)

    benford_ratios = [0.30103, 0.176091, 0.124939, 0.09691, 0.0791812, 0.0669468, 0.0579919, 0.0511525, 0.0457575]

    if benford_ratios[0] > max_value:
        max_value = benford_ratios[0]

    bar_graph = ""
    for i in range(0, 9):
        width = math.ceil((ratios[i] / max_value) * max_width)
        bar_graph += "*" * width
        bar_graph += " " * (max_width - width)
        bar_graph += f"   Leading {i+1} Ratio: {format_ratio(ratios[i])}"
        bar_graph += "\n"

        width_expected = math.ceil((benford_ratios[i] / max_value) * max_width)
        bar_graph += " " * (width_expected - 1)
        bar_graph += "^"
        bar_graph += " " * (max_width - width_expected)
        bar_graph += f"   Expected Ratio:  {format_ratio(benford_ratios[i])}"
        bar_graph += "\n"

        bar_graph += "\n"

    return bar_graph


def format_ratio(ratio):
    percentage = ratio * 100
    return f"{percentage:3.3f}%"
