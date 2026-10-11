# -*- coding: utf-8 -*-
"""Restitution proposée de chaque télégramme : texte ponctué, caractères rétablis entre accolades {x}.

Ce sont des PROPOSITIONS de lecture (Brice Dudout et Claude), non vérifiées une à une sur l'image. Chaque caractère
rétabli est justifié par le sens et par la proximité de ses lettres avec celles lues (le script calcule le nombre de
lettres à changer et le mécanisme : Morse, copie, autre). Le texte décodé et les lettres lues ne sont jamais modifiés.

Niveaux : 'P' = probable (une lettre, mécanisme plausible ou autre lecture, sens nettement meilleur, ou preuve extérieure) ;
          'Q' = possible (deux lettres, ou un seul indice).
Raisons : sens (sens de la phrase), contexte (autres télégrammes, histoire), structure (formule, numérotation, convention de
date), jumeau (télégramme parallèle), lecture (une autre lecture du formulaire donne ce caractère).
Les caractères douteux non rétablis restent entre ‹ ›. Le build vérifie que, accolades et ponctuation ôtées, le texte
coïncide caractère pour caractère avec le décodage."""

R = {
 '0455b': ('攝機係代滇購。如參部電詢，祈回電贊成。伸。元。', []),
 '0416b': ('報傳取消，日人態度遽變，確否速示，俾便行止。伸。{皓}。', [('P', ['jumeau', 'structure'])]),
 '0462': ('文內悉。前辦車需品，向興華所借款，務祈照辦，否則對滇信用未免掃地。粤事畢，前辦第二批械，務祈以北給滇，免貽口實。如何？盼覆。伸。卅。', []),
 '0348': ('三十式槍萬一千並軍用品已到門司，價作暫借，年息一割，無擔保。惟小池主，候尊電方運粤，{乞}速電催，萬勿謝絶，免負賠償。再，密碼私{單}已通。請逕復關正雄。伸令。漾。',
          [('P', ['sens', 'structure']), ('Q', ['sens'])]),
 '0415': ('據參部接山縣電，謂此次所器全未候滇，困難莫名，參部亦頗失望。伸在滇時已允一師，今次之半，{須}{其}一部。{如}不刁給，是械{款}兩端均置滇‹襯›不顧，如人言何？務祈如數分助，免滋物議。如何？盼復。伸。巧。',
          [('Q', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens', 'lecture'])]),
 '0386': ('文‹潌›電達。軍器飛機‹昱›午自頗坎發，陸日可到。萬密準{來}日宜歸滬，{準}仍來東。伸留，並聞準。伸令。卄。',
          [('Q', ['sens']), ('Q', ['sens'])]),
 '0406': ('段無組織內閣之{誠}意及能力。日{政}{府}現已同感，對{于}軍務院{及}南方全般{之}誤解，已夕牡消除。今後以不改豫定計畫爲限，可{望}終局援助。塞械仍大岸望，屢電‹逌›無復，礙難行動。席代轉‹逌›‹粤›促復。盼復。伸文文。',
          [('P', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens'])]),
 '0413': ('{擬}以建設航空隊之目的，購最{新}式軍用飛{行}機四台，並{聘}飛行家鈴木茂爲教官，款由東籌。贊否速示。伸。篠。',
          [('P', ['sens', 'structure']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens'])]),
 '0416a': ('滇索槍萬枝可辦到。因報傳軍院取消，方針遽變，確否速示，俾便行止。伸。皓。', []),
 '0449': ('伸爲滇訂最新軍用飛機六、無綫電機八。祈電岑轉參謀部，免生{障}{礙}。{武}器交涉中。並聞。齊。',
          [('P', ['sens', 'lecture']), ('P', ['sens', 'lecture']), ('P', ['sens', 'contexte'])]),
 '0455a': ('真電悉。武器及飛機事尚無結果，礙難卽歸。議會事祈照章以副議長{代}，{勿}往。伸。元。',
           [('P', ['sens', 'lecture']), ('P', ['sens', 'lecture'])]),
 '0467': ('記念章及各伊‹钎›盒‹侀›須九千五{百}元，如訂，祈匯款。詳{由}嘉{君}函呈。刻寺入內閣成立，武器或可有{望}，不日確定，卽歸。伸。灰。',
          [('P', ['sens']), ('P', ['sens', 'lecture']), ('Q', ['sens']), ('P', ['sens'])]),
 '0473': ('借款以·債爲標準，額{百}萬，息八釐，一‹矸›還，無擔保，九四{扣}。如借，祈飭伸簽約，卽交。速示。械須中央認可，當局始{允}侵給。並聞。回電祈相{京}{赤}{坂}青山南町‹孵›‹眥›。',
          [('P', ['sens']), ('P', ['sens', 'contexte']), ('P', ['sens']), ('Q', ['contexte']), ('Q', ['contexte', 'lecture']), ('Q', ['contexte'])]),
 '0489a': ('擬十號南歸，謹聞。伸。歌。', []),
 '0494a': ('歐戰{中}，卽內{債}{亦}無出九五扣者，俄且然，何况滇{無}抵押，應稍貴。餘{可}商，此難辦，擬歸商。盼立復。伸。尤。',
           [('P', ['sens']), ('Q', ['sens', 'contexte']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens'])]),
 '0496a': ('轉省議會及各報‹镱›：蔡公于八號午前二{時}病故福岡。公功德如山，應公布全滇，竭誠哀悼，並妥籌善後及記念。伸。{青}。',
           [('P', ['sens']), ('Q', ['structure'])]),
 '0498': ('{卅}、東兩電均悉。借款事舉‹剜›‹勳›妥爲接洽，{甚}感。但尚須‹澹›‹瀉›數事：一、款{額}擬‹簏›二三{百}萬{元}；二、年息擬六厘至七厘；三、攤四之期，至少{以}三年爲限；{四}、折{扣}之數，{最}大以{九}八爲率。以上四卽，{請}再向商榷。滇因需財留急，頗有此事之有成。如借額、攤{還}、折扣三事{可}以槪允，則年息尚可稍寬也。結果如何？盼復。',
          [('P', ['structure', 'sens']), ('P', ['sens']), ('P', ['sens', 'structure']), ('P', ['sens']), ('Q', ['structure']), ('P', ['sens']),
           ('P', ['structure']), ('Q', ['sens', 'structure']), ('P', ['sens']), ('P', ['sens']), ('P', ['sens']), ('P', ['structure', 'sens']), ('P', ['sens'])]),
}

PUNCT = set('。，、；：？！ ')


def parse(text, chars):
    """Renvoie la liste des jetons [(caractère affiché, index du code ou None, proposé?)] et la liste des index proposés.
    Vérifie l'alignement avec les caractères décodés (‹x› = caractère décodé laissé douteux)."""
    toks, props, i, k = [], [], 0, 0
    while k < len(text):
        c = text[k]
        if c in PUNCT:
            toks.append((c, None, False)); k += 1; continue
        if c == '{':
            ch = text[k + 1]; assert text[k + 2] == '}', text[k:k + 3]
            toks.append((ch, i, True)); props.append(i); i += 1; k += 3; continue
        if c == '‹':
            ch = text[k + 1]; assert text[k + 2] == '›'
            assert chars[i] == ch, ('douteux', i, ch, chars[i]); toks.append((ch, i, False)); i += 1; k += 3; continue
        assert chars[i] == c, ('écart', i, c, chars[i], text[max(0, k - 5):k + 5])
        toks.append((c, i, False)); i += 1; k += 1
    assert i == len(chars), ('longueur', i, len(chars))
    return toks, props
