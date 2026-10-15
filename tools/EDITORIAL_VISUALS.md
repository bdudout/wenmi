# Repères visuels du site

`editorial_visuals.py` est appelé par le build, après les illustrations existantes. Les textes restent natifs et adaptatifs, avec les couleurs du thème du site. Aucun script, police ou média distant n’est chargé.

- Accueil : frise de sept événements, dates ISO affichées sans ambiguïté, catégories textuelles (télégrammes, contexte, chiffre non déchiffré) et liens vers les passages justificatifs. Les espacements ne représentent pas la durée. L’attribution des messages Rosamonde au couple reste distincte de la date du formulaire.
- Méthode : comparaison de Rosamonde, du code télégraphique public, des condensateurs comme famille de tables, et des grilles particulières G0/Y0 du Wenmi de 1916. Le code public n’est pas présenté comme un secret, ni G0 comme une clé universelle.
- Méthode, transcription : formulaire JACAR du 7 juillet 1915, groupe `gowoisrjat` → `bemerciful` → `be merciful`, puis traduction. La clé est importée du schéma Rosamonde et le résultat est vérifié par assertion. La lacune après « Lovesick » dans le texte publié reste signalée.
- Trois cartes d’accueil réemploient les images locales existantes ; le recadrage est seulement visuel (CSS). Aucun original n’est modifié.

Références : corps multilingues de `content/`, en particulier `rosamonde.html#1915`, `history.html#chine`, `history.html#telegraphe`, `method.html#g0`, `relecture.html#principe`, `telegrams.html#t0509a`. Le mariage du 25 octobre 1915 renvoie à la [notice du musée de Shanghai](https://sswgw.org.cn/wwdc/szsww/4202.htm), déjà utilisée pour les illustrations de Rosamonde.

Vérification : `python3 tools/build.py`, `python3 tools/check_editorial_visuals.py`, `python3 tools/check_rosamonde_illustrations.py`. Les changements préexistants des contenus et les archives sont conservés. Aucune publication distante automatique.
