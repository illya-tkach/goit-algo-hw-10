"""Завдання 1. Видача решти: жадібний алгоритм vs динамічне програмування."""

import timeit

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount, coins=COINS):
    """Жадібно бере найбільший доступний номінал, поки сума не стане нулем.

    Складність: O(k), де k — кількість номіналів (на кожен номінал одна
    операція цілочисельного ділення).
    """
    result = {}
    remaining = amount
    for coin in sorted(coins, reverse=True):
        count, remaining = divmod(remaining, coin)
        if count:
            result[coin] = count
    if remaining:
        raise ValueError(f"Суму {amount} неможливо видати монетами {coins}")
    return result


def find_min_coins(amount, coins=COINS):
    """Знаходить мінімальну кількість монет методом динамічного програмування.

    min_coins[s] — мінімальна кількість монет для суми s,
    last_coin[s] — монета, якою закінчується оптимальний набір для суми s.
    Складність: O(n * k) за часом і O(n) за пам'яттю, де n — сума.
    """
    coins = sorted(coins)
    min_coins = [0] + [float("inf")] * amount
    last_coin = [0] * (amount + 1)

    for s in range(1, amount + 1):
        for coin in coins:
            if coin > s:
                break
            if min_coins[s - coin] + 1 < min_coins[s]:
                min_coins[s] = min_coins[s - coin] + 1
                last_coin[s] = coin

    if min_coins[amount] == float("inf"):
        raise ValueError(f"Суму {amount} неможливо видати монетами {coins}")

    result = {}
    s = amount
    while s > 0:
        coin = last_coin[s]
        result[coin] = result.get(coin, 0) + 1
        s -= coin
    return dict(sorted(result.items()))


def measure(func, amount, repeat=3):
    """Найкращий час одного виклику функції (у секундах)."""
    number = 1 if amount >= 10_000 else 10
    times = timeit.repeat(lambda: func(amount), number=number, repeat=repeat)
    return min(times) / number


def main():
    amount = 113
    print(f"Сума: {amount}")
    print(f"  find_coins_greedy: {find_coins_greedy(amount)}")
    print(f"  find_min_coins:    {find_min_coins(amount)}")

    print("\nПорівняння часу виконання:")
    print(f"{'Сума':>10} | {'Жадібний, с':>12} | {'ДП, с':>12} | {'ДП / жадібний':>14} | Монет (ж / дп)")
    print("-" * 78)
    for amount in (10, 113, 1_000, 10_000, 100_000, 1_000_000):
        greedy = find_coins_greedy(amount)
        dp = find_min_coins(amount)
        t_greedy = measure(find_coins_greedy, amount)
        t_dp = measure(find_min_coins, amount)
        print(
            f"{amount:>10} | {t_greedy:>12.2e} | {t_dp:>12.2e} | {t_dp / t_greedy:>13.0f}x | "
            f"{sum(greedy.values())} / {sum(dp.values())}"
        )

    # Для неканонічного набору монет жадібний алгоритм не завжди оптимальний.
    coins, amount = [1, 3, 4], 6
    print(f"\nНеканонічний набір {coins}, сума {amount}:")
    print(f"  find_coins_greedy: {find_coins_greedy(amount, coins)}")
    print(f"  find_min_coins:    {find_min_coins(amount, coins)}")


if __name__ == "__main__":
    main()
