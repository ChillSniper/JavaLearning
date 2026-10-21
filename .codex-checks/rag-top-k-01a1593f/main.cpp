#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d, k;
    if (!(cin >> n >> d >> k)) return 0;

    vector<int> documents(n * d);
    for (int& value : documents) cin >> value;

    vector<int> query(d);
    for (int& value : query) cin >> value;

    vector<pair<long long, int>> results(n);
    for (int i = 0; i < n; ++i) {
        long long score = 0;
        for (int j = 0; j < d; ++j) {
            score += 1LL * documents[i * d + j] * query[j];
        }
        results[i] = {score, i + 1};
    }

    sort(results.begin(), results.end(), [](const auto& a, const auto& b) {
        if (a.first != b.first) return a.first > b.first;
        return a.second < b.second;
    });

    for (int i = 0; i < k; ++i) {
        cout << results[i].second << '\n';
    }
    return 0;
}
