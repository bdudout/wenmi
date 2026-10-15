"""Date et heure lues sur les formulaires (séance YC, 15/10/2026), pour classer les télégrammes par date et heure.
Heure = case « Time » de l'en-tête (dépôt au bureau d'origine) ; à défaut « Time Sent » (0348). None : feuillet de suite
sans en-tête, ou heure « nil » (formulaire de réception). Format identique à corpus-n1916.js (« 5.35 pm »)."""
# Wenmi (corpus.js) : (mois, jour) et heure
WENMI = {'0348': ((6, 23), '8.13 pm'), '0386': ((6, 30), '2.45 pm'), '0406': ((7, 12), '2.50 pm'), '0413': ((7, 17), '4.30 pm'),
         '0415': ((7, 18), '5.30 pm'), '0416a': ((7, 19), '5.50 pm'), '0416b': ((7, 19), '5.50 pm'), '0449': ((9, 8), '7 pm'),
         '0455a': ((9, 13), '7.30 pm'), '0455b': ((9, 13), '7.30 pm'), '0462': ((9, 30), '11 am'), '0467': ((10, 11), '5.46 pm'),
         '0473': ((10, 20), '7.30 pm'), '0489a': ((11, 5), '11.55 am'), '0494a': ((11, 11), '8.35 pm'), '0496a': ((11, 9), '6.25 pm'),
         '0498': ((11, 9), '2.35 pm')}   # 0498 : « 14-35 » à Yunnanfu (reçu à Aoyama le 10/11, 7.40 pm)
# condensateurs 1916 (corpus-c1916.js, id) : heure seulement (la date est déjà dans les données)
C1916 = {'c0470': '8.45 pm', 'c0445': '11.50 am', 'c0461b': None, 'c0478a': None, 'c0468': '12.42 pm', 'c0465a': '2.40 pm',
         'c0460': None, 'c0473a': '12.45 pm', 'c0475': '12.45 pm', 'c0485': '9.15 pm', 'c0486a': '7.40 pm', 'c0489': '6.37 pm',
         'c0495': None, 'c0459': None, 'c0473b': '12.45 pm', 'c0476': '8.50 am', 'c0490b': None, 'c0492': '4.25 pm',
         'c0061': '8.10 pm', 'c0069': None, 'c0071': '5.40 pm', 'c0075': '1.20 pm', 'c0087': '5 pm', 'c0092': '10.25 am'}


def minutes(t):
    """« 5.35 pm » → minutes depuis minuit (None → fin de journée, pour le tri)."""
    if not t:
        return 24 * 60
    hm, ap = t.split()
    h, m = (hm.split('.') + ['0'])[:2]
    h, m = int(h), int(m)
    if ap == 'pm' and h != 12:
        h += 12
    if ap == 'am' and h == 12:
        h = 0
    return h * 60 + m

# télégrammes de 1915 (corpus-t1915.js, id de t1915_data.json) : heure de dépôt ; None = formulaire de réception sans heure de dépôt
T1915 = {'t1915-0106m': '3.40 pm', 't1915-0131': '6 pm', 't1915-02p23': '6 pm', 't1915-0202': '3.42 pm', 't1915-0218': None,
         't1915-0220': None, 't1915-02ny': None, 't1915-0226': '3.32 pm', 't1915-0227': '11.43 am', 't1915-0307': '11.12 am',
         't1915-0310': '11.10 am'}
# jour approché pour le classement seulement (date illisible sur le formulaire) : 02p23 entre les images du 31/1 et du 2/2 ;
# 02ny lu « 29/2 », vers le 24/2 (working/c35/inedits-1915.md)
T1915_SORT_DAY = {'t1915-02p23': 1, 't1915-02ny': 24}
