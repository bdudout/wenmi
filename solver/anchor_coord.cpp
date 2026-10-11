// C31 — E17 : solveur à table de COORDONNÉES (H9) : la consonne code la dizaine du demi-code (20 consonnes = 10 dizaines × 2
// homophones), la voyelle + le choix de l'homophone codent l'unité. La table reste une bijection unité -> 00..99, mais
// structurée ; les mouvements du recuit préservent la structure :
//   (M1) échange de deux consonnes, valeurs échangées voyelle à voyelle (10 unités changent de valeur ; dizaines et jeux d'unités échangés) ;
//   (M2) échange des valeurs de deux unités de MÊME dizaine (même consonne, ou les deux homophones).
// Dérivé de anchor_arr.cpp (mêmes LM3, scoring incrémental, ILS, arrangement/retenue/KHI facultatifs).
// Usage : anchor_coord <job.txt> <out.tsv> <restarts> <iters> <seed> [threads] [ils_rounds ils_iters ils_k ils_T0] [arr] [T] [khi] [pblock]
// job.txt : LM <dir> / TYPES u1 … u100 (les 100 unités, consonne-majeur) / MSG <name> u1 u2 … ("--" = masque) / ANCHOR u v / TRUTH u v
#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <map>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

static float UNI[10000]; static double REF = 0;
static std::vector<uint32_t> HK; static std::vector<float> HV; static uint32_t HMASK;
static float BDEF = 0.f;
static int ARR[4] = {0, 1, 2, 3}; static int KHI = 0; static int TBORROW = 100; static double PBLOCK = 0.1;
static inline int assemble(int va, int vb) {
    int d[4] = {va / 10, va % 10, vb / 10, vb % 10};
    int hi = d[ARR[0]] * 10 + d[ARR[1]], lo = d[ARR[2]] * 10 + d[ARR[3]];
    if (TBORROW > 0) { if (lo >= TBORROW) hi = (hi + 99) % 100; }
    else if (TBORROW < 0) { if (lo <= -TBORROW) hi = (hi + 1) % 100; }
    hi = (hi + KHI) % 100;
    return hi * 100 + lo;
}
static inline float bonus(int a, int b) {
    uint32_t k = (uint32_t)a * 10000u + (uint32_t)b + 1u, h = (k * 2654435761u) & HMASK;
    while (HK[h]) { if (HK[h] == k) return HV[h]; h = (h + 1) & HMASK; }
    return BDEF;
}
static void load_lm(const std::string& d) {
    FILE* f = fopen((d + "/uni.f32").c_str(), "rb"); if (!f || fread(UNI, 4, 10000, f) != 10000) exit(2); fclose(f);
    for (int i = 0; i < 10000; i++) REF += UNI[i]; REF /= 10000;
    { FILE* g = fopen((d + "/bidef.f32").c_str(), "rb"); if (g) { if (fread(&BDEF, 4, 1, g) != 1) BDEF = 0; fclose(g); } }
    f = fopen((d + "/bi.u32").c_str(), "rb"); fseek(f, 0, SEEK_END); long n = ftell(f) / 4; fseek(f, 0, SEEK_SET);
    std::vector<uint32_t> K(n); std::vector<float> V(n);
    if ((long)fread(K.data(), 4, n, f) != n) exit(2); fclose(f);
    f = fopen((d + "/bi.f32").c_str(), "rb"); if ((long)fread(V.data(), 4, n, f) != n) exit(2); fclose(f);
    uint32_t cap = 1; while (cap < 4 * (uint32_t)n) cap <<= 1; HK.assign(cap, 0); HV.assign(cap, 0); HMASK = cap - 1;
    for (long i = 0; i < n; i++) { uint32_t k = K[i] + 1u, h = (k * 2654435761u) & HMASK; while (HK[h]) h = (h + 1) & HMASK; HK[h] = k; HV[h] = V[i]; }
}
struct Code { int a, b, msg, prev, next; };

int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    int restarts = atoi(argv[3]); long iters = atol(argv[4]); unsigned seed = (unsigned)atol(argv[5]);
    int threads = argc > 6 ? atoi(argv[6]) : 8;
    const int ilsRounds = argc > 7 ? atoi(argv[7]) : 0; const long ilsIters = argc > 8 ? atol(argv[8]) : 0;
    const int ilsK = argc > 9 ? atoi(argv[9]) : 6; const double ilsT0 = argc > 10 ? atof(argv[10]) : 0.6;
    if (argc > 11) { const char* s = argv[11]; for (int i = 0; i < 4; i++) ARR[i] = s[i] - '1'; }
    if (argc > 12) TBORROW = atoi(argv[12]);
    if (argc > 13) KHI = ((atoi(argv[13]) % 100) + 100) % 100;
    if (argc > 14) PBLOCK = atof(argv[14]);
    std::ifstream in(argv[1]); std::string line, lmdir;
    std::map<std::string, int> tid; std::vector<std::string> tname;
    std::vector<std::vector<int>> msgs; std::vector<std::string> mnames;
    std::vector<std::pair<int,int>> anchors, truth;
    auto T = [&](const std::string& u) { auto it = tid.find(u); if (it != tid.end()) return it->second;
        int k = (int)tname.size(); tid[u] = k; tname.push_back(u); return k; };
    while (std::getline(in, line)) {
        std::istringstream ss(line); std::string tag; ss >> tag;
        if (tag == "LM") std::getline(ss >> std::ws, lmdir);
        else if (tag == "TYPES") { std::string u; while (ss >> u) T(u); }
        else if (tag == "MSG") { std::string n, u; ss >> n; std::vector<int> m;
            while (ss >> u) m.push_back(u == "--" ? -1 : T(u)); msgs.push_back(m); mnames.push_back(n); }
        else if (tag == "ANCHOR") { std::string u; int v; ss >> u >> v; anchors.push_back({T(u), v}); }
        else if (tag == "TRUTH") { std::string u; int v; ss >> u >> v; truth.push_back({T(u), v}); }
    }
    load_lm(lmdir);
    const int NT = (int)tname.size();
    // alphabets : consonne = 1re lettre, voyelle = 2e lettre, dans l'ordre d'apparition (TYPES d'abord)
    std::vector<int> ci(NT), vi(NT); std::string cons, vows;
    for (int t = 0; t < NT; t++) { if (tname[t].size() != 2) { fprintf(stderr, "type %s\n", tname[t].c_str()); return 3; }
        size_t p = cons.find(tname[t][0]); if (p == std::string::npos) { p = cons.size(); cons += tname[t][0]; } ci[t] = (int)p;
        size_t q = vows.find(tname[t][1]); if (q == std::string::npos) { q = vows.size(); vows += tname[t][1]; } vi[t] = (int)q; }
    const int NCONS = (int)cons.size(), NVOW = (int)vows.size();
    if (NCONS != 20 || NVOW != 5 || NT != 100) { fprintf(stderr, "alphabet %d x %d, types %d (attendu 20 x 5 = 100 via TYPES)\n", NCONS, NVOW, NT); return 3; }
    std::vector<std::vector<int>> unitOf(NCONS, std::vector<int>(NVOW, -1));
    for (int t = 0; t < NT; t++) unitOf[ci[t]][vi[t]] = t;
    std::vector<Code> codes;
    for (size_t mi = 0; mi < msgs.size(); mi++) {
        int last = -1; const auto& m = msgs[mi];
        for (size_t i = 0; i + 1 < m.size(); i += 2) {
            if (m[i] < 0 || m[i + 1] < 0) { last = -1; continue; }
            Code c{m[i], m[i + 1], (int)mi, last, -1}; codes.push_back(c);
            if (last >= 0) codes[last].next = (int)codes.size() - 1; last = (int)codes.size() - 1; } }
    const int NC = (int)codes.size();
    std::vector<std::vector<int>> occ(NT);
    for (int c = 0; c < NC; c++) { occ[codes[c].a].push_back(c); if (codes[c].b != codes[c].a) occ[codes[c].b].push_back(c); }
    // ancres : dizaine de la consonne + unité ; faisabilité
    std::vector<int> fixedv(NT, -1), fixedTens(NCONS, -1); std::vector<char> consAnch(NCONS, 0);
    for (auto& a : anchors) { int t = a.first, c = ci[t], tens = a.second / 10;
        if (fixedv[t] >= 0 && fixedv[t] != a.second) { fprintf(stderr, "ancre contradictoire %s\n", tname[t].c_str()); return 3; }
        if (fixedTens[c] >= 0 && fixedTens[c] != tens) { fprintf(stderr, "ancres incompatibles (dizaine) consonne %c\n", cons[c]); return 3; }
        fixedv[t] = a.second; fixedTens[c] = tens; consAnch[c] = 1; }
    { std::vector<int> cnt(10, 0); for (int c = 0; c < NCONS; c++) if (fixedTens[c] >= 0) cnt[fixedTens[c]]++;
      for (int g = 0; g < 10; g++) if (cnt[g] > 2) { fprintf(stderr, "ancres infaisables : %d consonnes pour la dizaine %d\n", cnt[g], g); return 3; }
      std::vector<char> used(100, 0); for (int t = 0; t < NT; t++) if (fixedv[t] >= 0) { if (used[fixedv[t]]) { fprintf(stderr, "ancres : valeur %d en double\n", fixedv[t]); return 3; } used[fixedv[t]] = 1; } }
    std::vector<int> freeT; for (int t = 0; t < NT; t++) if (fixedv[t] < 0) freeT.push_back(t);
    fprintf(stderr, "types=%d free=%zu codes=%d anchors=%zu REF=%.3f BDEF=%.3f arr=%d%d%d%d T=%d khi=%d pblock=%.2f\n", NT, freeT.size(), NC, anchors.size(), REF, BDEF, ARR[0]+1, ARR[1]+1, ARR[2]+1, ARR[3]+1, TBORROW, KHI, PBLOCK);
    struct Res { double score; std::vector<int> v; };
    std::vector<Res> results(restarts); std::atomic<int> next(0);
    auto worker = [&](int wid) {
        std::vector<int> v(NT), owner(100), cv(NC), mark(NC, 0), tens(NCONS); int stamp = 0;
        std::vector<int> aff; aff.reserve(4 * NC); std::vector<int> saved; saved.reserve(4 * NC);
        std::vector<std::pair<int,int>> chg; chg.reserve(16);
        for (;;) {
            int r = next.fetch_add(1); if (r >= restarts) break;
            std::mt19937_64 rng(seed * 1000003ull + r); std::uniform_real_distribution<double> U(0, 1);
            auto codeOf = [&](int c) { return assemble(v[codes[c].a], v[codes[c].b]); };
            double S = 0;
            auto recompute = [&]() { std::fill(owner.begin(), owner.end(), -1); for (int t = 0; t < NT; t++) owner[v[t]] = t; S = 0;
                for (int c = 0; c < NC; c++) { cv[c] = codeOf(c); S += UNI[cv[c]] - REF; if (codes[c].prev >= 0) S += bonus(cv[codes[c].prev], cv[c]); } };
            // init : table de coordonnées aléatoire compatible avec les ancres
            { std::vector<int> slots; std::vector<int> cnt(10, 0);
              for (int c = 0; c < NCONS; c++) tens[c] = fixedTens[c]; for (int c = 0; c < NCONS; c++) if (tens[c] >= 0) cnt[tens[c]]++;
              for (int g = 0; g < 10; g++) for (int k = cnt[g]; k < 2; k++) slots.push_back(g);
              std::shuffle(slots.begin(), slots.end(), rng); size_t si = 0;
              std::vector<int> order(NCONS); for (int c = 0; c < NCONS; c++) order[c] = c; std::shuffle(order.begin(), order.end(), rng);
              for (int c : order) if (tens[c] < 0) tens[c] = slots[si++];
              for (int g = 0; g < 10; g++) { std::vector<int> units, digs; std::vector<char> usedd(10, 0);
                  for (int c = 0; c < NCONS; c++) if (tens[c] == g) for (int w = 0; w < NVOW; w++) { int t = unitOf[c][w];
                      if (fixedv[t] >= 0) { v[t] = fixedv[t]; usedd[fixedv[t] % 10] = 1; } else units.push_back(t); }
                  for (int d = 0; d < 10; d++) if (!usedd[d]) digs.push_back(d);
                  std::shuffle(digs.begin(), digs.end(), rng); for (size_t i = 0; i < units.size(); i++) v[units[i]] = 10 * g + digs[i]; } }
            recompute();
            double best = S; std::vector<int> bestv = v;
            auto apply = [&](double Tt, bool force, int c1, int c2) {   // chg rempli ; c1/c2 >= 0 : échange de dizaines à entériner
                stamp++; aff.clear();
                for (auto& p : chg) for (int c : occ[p.first]) if (mark[c] != stamp) { mark[c] = stamp; aff.push_back(c); }
                double old = 0;
                for (int c : aff) { old += UNI[cv[c]]; int p = codes[c].prev; if (p >= 0) old += bonus(cv[p], cv[c]);
                    int n = codes[c].next; if (n >= 0 && mark[n] != stamp) old += bonus(cv[c], cv[n]); }
                saved.clear(); for (auto& p : chg) { saved.push_back(v[p.first]); v[p.first] = p.second; }
                std::vector<int> savedcv; savedcv.reserve(aff.size());
                for (int c : aff) { savedcv.push_back(cv[c]); cv[c] = codeOf(c); }
                double nw = 0;
                for (int c : aff) { nw += UNI[cv[c]]; int p = codes[c].prev; if (p >= 0) nw += bonus(cv[p], cv[c]);
                    int n = codes[c].next; if (n >= 0 && mark[n] != stamp) nw += bonus(cv[c], cv[n]); }
                double d = nw - old;
                if (force || d >= 0 || U(rng) < std::exp(d / Tt)) {
                    S += d; for (auto& p : chg) owner[p.second] = p.first; if (c1 >= 0) std::swap(tens[c1], tens[c2]);
                    if (S > best) { best = S; bestv = v; }
                } else {
                    for (size_t i = 0; i < chg.size(); i++) v[chg[i].first] = saved[i];
                    for (size_t i = 0; i < aff.size(); i++) cv[aff[i]] = savedcv[i];
                }
            };
            auto step = [&](double Tt, bool force) {
                chg.clear();
                if (U(rng) < PBLOCK) {   // M1 : échange des dizaines de deux consonnes
                    int c1 = (int)(rng() % NCONS), c2 = (int)(rng() % NCONS); if (c1 == c2 || consAnch[c1] || consAnch[c2]) return;
                    // échange des deux consonnes (valeurs échangées voyelle à voyelle) : préserve la bijection ET la structure (c1 prend la dizaine et le jeu d'unités de c2, et réciproquement)
                    for (int w = 0; w < NVOW; w++) { chg.push_back({unitOf[c1][w], v[unitOf[c2][w]]}); chg.push_back({unitOf[c2][w], v[unitOf[c1][w]]}); }
                    apply(Tt, force, c1, c2);
                } else {                 // M2 : échange de deux unités de même dizaine
                    int t1 = freeT[rng() % freeT.size()]; int w = (v[t1] / 10) * 10 + (int)(rng() % 10); int t2 = owner[w];
                    if (t2 == t1 || fixedv[t2] >= 0) return;
                    chg.push_back({t1, w}); chg.push_back({t2, v[t1]}); apply(Tt, force, -1, -1);
                }
            };
            auto anneal = [&](double T0, double T1, long n) { for (long it = 0; it < n; it++) step(T0 * std::pow(T1 / T0, (double)it / n), false); };
            anneal(3.0, 0.03, iters);
            for (int k = 0; k < ilsRounds; k++) { v = bestv; recompute(); for (int c = 0; c < NCONS; c++) tens[c] = v[unitOf[c][0]] / 10;
                for (int j = 0; j < ilsK; j++) step(1.0, true); anneal(ilsT0, 0.03, ilsIters); }
            results[r] = {best, bestv};
        }
    };
    std::vector<std::thread> th; for (int i = 0; i < threads; i++) th.emplace_back(worker, i);
    for (auto& t : th) t.join();
    std::sort(results.begin(), results.end(), [](const Res& a, const Res& b) { return a.score > b.score; });
    FILE* o = fopen(argv[2], "w"); fprintf(o, "#types"); for (int t = 0; t < NT; t++) fprintf(o, "\t%s", tname[t].c_str()); fprintf(o, "\n");
    for (auto& r : results) { int ok = 0; for (auto& tr : truth) ok += r.v[tr.first] == tr.second;
        fprintf(o, "%.4f\t%d/%zu", r.score, ok, truth.size()); for (int t = 0; t < NT; t++) fprintf(o, "\t%d", r.v[t]); fprintf(o, "\n"); }
    fclose(o);
    int ok = 0; for (auto& tr : truth) ok += results[0].v[tr.first] == tr.second;
    fprintf(stderr, "best=%.3f second=%.3f truth_units=%d/%zu\n", results[0].score, results.size() > 1 ? results[1].score : 0, ok, truth.size());
    return 0;
}
