// Exact exhaustive census for the deployed M31 order-32 Chebyshev quotient.
//
// For each omitted quotient label, this program enumerates every 17-subset of
// the remaining 31 labels, sorts their sums in F_p, and reports the complete
// sum-fibre maximum.  The computation is exact: the meet-in-the-middle split
// reduces subset generation work but does not sample or discard any subset.
//
// Build:
//   c++ -O3 -std=c++17 \
//     experimental/scripts/verify_m31_chebyshev_order32_sum_fiber_census_v1.cpp \
//     -o /tmp/verify_m31_cheb32_sum_fiber
//
// Run one omission or all omissions sequentially:
//   /tmp/verify_m31_cheb32_sum_fiber 0
//   /tmp/verify_m31_cheb32_sum_fiber --all

#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string_view>
#include <vector>

namespace {

constexpr std::uint32_t kPrime = 2147483647u;
constexpr unsigned kSubsetSize = 17;
constexpr std::uint64_t kExpectedSubsetCount = 265182525u;
constexpr std::uint64_t kExpectedStructuralFamilyCount = 6435u;

// The deployed quotient labels, in the normalization used by the packet.
// They are the 32 distinct roots of T_32(2Y) over F_{2^31-1}.
constexpr std::array<std::uint32_t, 32> kLabels = {
    1515618352u, 2142581798u,  519472958u,  942646298u,
     419097603u,    7265015u, 1945140650u, 1179963362u,
     970712266u, 1077313983u,  114254582u,  186614876u,
     869502427u, 1006664095u, 2113254329u, 1972112504u,
     175371143u,   34229318u, 1140819552u, 1277981220u,
    1960868771u, 2033229065u, 1070169664u, 1176771381u,
     967520285u,  202342997u, 2140218632u, 1728386044u,
    1204837349u, 1628010689u,    4901849u,  631865295u,
};

struct CensusResult {
  unsigned omitted = 0;
  std::uint64_t subset_count = 0;
  std::uint64_t distinct_sums = 0;
  std::uint64_t max_fiber = 0;
  std::uint32_t max_key = 0;
  std::uint64_t keys_at_max = 0;
  std::uint32_t structural_key = 0;
  std::uint64_t structural_family_count = 0;
  std::uint64_t structural_target_fiber = 0;
};

std::uint32_t add_mod(const std::uint32_t left,
                      const std::uint32_t right) {
  const std::uint64_t sum =
      static_cast<std::uint64_t>(left) + static_cast<std::uint64_t>(right);
  return static_cast<std::uint32_t>(sum >= kPrime ? sum - kPrime : sum);
}

std::uint32_t negate_mod(const std::uint32_t value) {
  return value == 0 ? 0 : kPrime - value;
}

std::uint64_t binomial(unsigned n, unsigned k) {
  if (k > n) return 0;
  if (k > n - k) k = n - k;
  std::uint64_t value = 1;
  for (unsigned i = 1; i <= k; ++i) {
    value = value * static_cast<std::uint64_t>(n - k + i) / i;
  }
  return value;
}

bool validate_deployed_labels() {
  std::uint32_t total = 0;
  for (std::size_t i = 0; i < kLabels.size(); ++i) {
    if (kLabels[i] == 0 || kLabels[i] >= kPrime) {
      std::cerr << "invalid deployed label at index " << i << '\n';
      return false;
    }
    total = add_mod(total, kLabels[i]);
    unsigned negative_matches = 0;
    for (std::size_t j = 0; j < kLabels.size(); ++j) {
      if (i != j && kLabels[i] == kLabels[j]) {
        std::cerr << "duplicate deployed labels at indices " << i << " and "
                  << j << '\n';
        return false;
      }
      if (kLabels[j] == negate_mod(kLabels[i])) ++negative_matches;
    }
    if (negative_matches != 1) {
      std::cerr << "label at index " << i
                << " does not have exactly one antipode\n";
      return false;
    }
  }
  if (total != 0) {
    std::cerr << "deployed label sum is not zero\n";
    return false;
  }
  if (binomial(31, kSubsetSize) != kExpectedSubsetCount ||
      binomial(15, 8) != kExpectedStructuralFamilyCount) {
    std::cerr << "internal binomial constants are inconsistent\n";
    return false;
  }
  return true;
}

void enumerate_half(
    const std::vector<std::uint32_t>& values,
    const std::size_t index,
    const unsigned cardinality,
    const std::uint32_t sum,
    std::vector<std::vector<std::uint32_t>>& sums_by_size) {
  if (index == values.size()) {
    sums_by_size[cardinality].push_back(sum);
    return;
  }
  enumerate_half(values, index + 1, cardinality, sum, sums_by_size);
  enumerate_half(values, index + 1, cardinality + 1,
                 add_mod(sum, values[index]), sums_by_size);
}

bool derive_structural_family(const unsigned omitted,
                              std::uint32_t* structural_key,
                              std::uint64_t* structural_count) {
  if (structural_key == nullptr || structural_count == nullptr) return false;
  const std::uint32_t target = negate_mod(kLabels[omitted]);
  std::size_t antipode_index = kLabels.size();
  for (std::size_t i = 0; i < kLabels.size(); ++i) {
    if (kLabels[i] == target) {
      antipode_index = i;
      break;
    }
  }
  if (antipode_index == kLabels.size() || antipode_index == omitted) {
    std::cerr << "failed to locate omitted label's antipode\n";
    return false;
  }

  // After deleting x and reserving -x, the other 30 labels must split into
  // 15 complete antipodal pairs.  Selecting both members of any eight pairs,
  // together with -x, gives a 17-subset of sum -x.
  std::array<bool, kLabels.size()> used{};
  used[omitted] = true;
  used[antipode_index] = true;
  unsigned pair_count = 0;
  for (std::size_t i = 0; i < kLabels.size(); ++i) {
    if (used[i]) continue;
    std::size_t partner = kLabels.size();
    for (std::size_t j = 0; j < kLabels.size(); ++j) {
      if (!used[j] && j != i && kLabels[j] == negate_mod(kLabels[i])) {
        partner = j;
        break;
      }
    }
    if (partner == kLabels.size()) {
      std::cerr << "residual labels fail to split into antipodal pairs\n";
      return false;
    }
    used[i] = true;
    used[partner] = true;
    ++pair_count;
  }
  if (pair_count != 15) {
    std::cerr << "unexpected residual antipodal-pair count " << pair_count
              << '\n';
    return false;
  }
  *structural_key = target;
  *structural_count = binomial(pair_count, 8);
  return true;
}

bool run_census(const unsigned omitted, CensusResult* result) {
  if (result == nullptr || omitted >= kLabels.size()) return false;

  std::uint32_t structural_key = 0;
  std::uint64_t structural_count = 0;
  if (!derive_structural_family(omitted, &structural_key,
                                &structural_count)) {
    return false;
  }

  std::vector<std::uint32_t> residual_labels;
  residual_labels.reserve(kLabels.size() - 1);
  for (unsigned i = 0; i < kLabels.size(); ++i) {
    if (i != omitted) residual_labels.push_back(kLabels[i]);
  }
  if (residual_labels.size() != 31) {
    std::cerr << "internal residual-label cardinality mismatch\n";
    return false;
  }

  // A 15+16 split materializes only 2^15+2^16 half sums before the exact
  // C(31,17)-entry multiset is assembled.
  const std::vector<std::uint32_t> left(residual_labels.begin(),
                                        residual_labels.begin() + 15);
  const std::vector<std::uint32_t> right(residual_labels.begin() + 15,
                                         residual_labels.end());
  std::vector<std::vector<std::uint32_t>> left_sums(left.size() + 1);
  std::vector<std::vector<std::uint32_t>> right_sums(right.size() + 1);
  enumerate_half(left, 0, 0, 0, left_sums);
  enumerate_half(right, 0, 0, 0, right_sums);

  std::vector<std::uint32_t> sums;
  if (kExpectedSubsetCount > sums.max_size()) {
    std::cerr << "host cannot represent the exhaustive sum multiset\n";
    return false;
  }
  sums.reserve(static_cast<std::size_t>(kExpectedSubsetCount));
  for (unsigned left_size = 0; left_size <= left.size(); ++left_size) {
    if (left_size > kSubsetSize) continue;
    const unsigned right_size = kSubsetSize - left_size;
    if (right_size > right.size()) continue;
    for (const std::uint32_t left_sum : left_sums[left_size]) {
      for (const std::uint32_t right_sum : right_sums[right_size]) {
        sums.push_back(add_mod(left_sum, right_sum));
      }
    }
  }
  if (sums.size() != kExpectedSubsetCount) {
    std::cerr << "exhaustive subset count mismatch: got " << sums.size()
              << ", expected " << kExpectedSubsetCount << '\n';
    return false;
  }

  std::sort(sums.begin(), sums.end());

  CensusResult computed;
  computed.omitted = omitted;
  computed.subset_count = sums.size();
  computed.structural_key = structural_key;
  computed.structural_family_count = structural_count;

  std::size_t run_begin = 0;
  while (run_begin < sums.size()) {
    std::size_t run_end = run_begin + 1;
    while (run_end < sums.size() && sums[run_end] == sums[run_begin]) {
      ++run_end;
    }
    const std::uint64_t run_size = run_end - run_begin;
    const std::uint32_t key = sums[run_begin];
    ++computed.distinct_sums;
    if (run_size > computed.max_fiber) {
      computed.max_fiber = run_size;
      computed.max_key = key;
      computed.keys_at_max = 1;
    } else if (run_size == computed.max_fiber) {
      ++computed.keys_at_max;
    }
    if (key == structural_key) computed.structural_target_fiber = run_size;
    run_begin = run_end;
  }

  // These checks turn the exact census into the advertised route-cut
  // verifier: the explicit antipodal family is not merely a lower bound; it
  // is the unique global maximum.
  if (computed.structural_family_count !=
          kExpectedStructuralFamilyCount ||
      computed.structural_target_fiber !=
          computed.structural_family_count ||
      computed.max_fiber != computed.structural_family_count ||
      computed.max_key != computed.structural_key ||
      computed.keys_at_max != 1) {
    std::cerr << "exact census did not match the structural maximum for "
              << "omission " << omitted << '\n';
    return false;
  }

  *result = computed;
  return true;
}

void print_result(const CensusResult& result) {
  std::cout << "CHEB32_SUM_CENSUS_V1"
            << " omitted=" << result.omitted
            << " omitted_label=" << kLabels[result.omitted]
            << " subsets=" << result.subset_count
            << " distinct=" << result.distinct_sums
            << " max_fiber=" << result.max_fiber
            << " max_key=" << result.max_key
            << " keys_at_max=" << result.keys_at_max
            << " structural_key=" << result.structural_key
            << " structural_family_count="
            << result.structural_family_count
            << " structural_target_fiber="
            << result.structural_target_fiber << " status=PASS\n";
}

bool parse_omission(const std::string_view text, unsigned* omitted) {
  if (omitted == nullptr || text.empty()) return false;
  unsigned parsed = 0;
  const char* const begin = text.data();
  const char* const end = begin + text.size();
  const auto conversion = std::from_chars(begin, end, parsed);
  if (conversion.ec != std::errc{} || conversion.ptr != end ||
      parsed >= kLabels.size()) {
    return false;
  }
  *omitted = parsed;
  return true;
}

void print_usage(const char* executable) {
  std::cerr << "usage: " << executable << " OMITTED_INDEX|--all\n"
            << "  OMITTED_INDEX must be an integer in [0,31].\n";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc == 2 && std::string_view(argv[1]) == "--help") {
    print_usage(argv[0]);
    return 0;
  }
  if (argc != 2) {
    print_usage(argv[0]);
    return 2;
  }
  if (!validate_deployed_labels()) return 3;

  if (std::string_view(argv[1]) == "--all") {
    for (unsigned omitted = 0; omitted < kLabels.size(); ++omitted) {
      CensusResult result;
      if (!run_census(omitted, &result)) return 4;
      print_result(result);
      std::cout.flush();
    }
    std::cout << "CHEB32_SUM_CENSUS_V1_ALL omissions=" << kLabels.size()
              << " status=PASS\n";
    return 0;
  }

  unsigned omitted = 0;
  if (!parse_omission(argv[1], &omitted)) {
    std::cerr << "invalid omission index: " << argv[1] << '\n';
    print_usage(argv[0]);
    return 2;
  }
  CensusResult result;
  if (!run_census(omitted, &result)) return 4;
  print_result(result);
  return 0;
}
