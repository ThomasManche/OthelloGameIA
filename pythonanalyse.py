# Fonction qui va créer ou mettre à jour l'index cle du dictionnaire dico avec sa victoire win ou son match nul is_nul
def maj(dico, cle, win, is_nul):
    if cle not in dico: dico[cle] = [0, 0, 0]
    dico[cle][2] += 1
    if win: dico[cle][0] += 1
    if is_nul: dico[cle][1] += 1


def analyse_finale_ia():
    f = open('resultat.txt', 'r', encoding='utf-8')
    contenu = f.read()
    f.close()

    parties = contenu.split('-----------------------')

    stats_ia_brutes = {}    
    stats_heuristiques = {} 
    stats_profondeur = {}   
    configs = {}            
    ecarts = {}             
    pions_totaux = {}       
    perfects = {}           
    nemesis = {}            
    ia_heuristiques = {}    
    victoires_data = {} 
    defaites_data = {}  

    ia_noeuds_total = {}    
    ia_temps_total = {}     
    ia_coups_total = {}     
    ia_matchs_count = {} 
    ia_depth_details = {} 
    ia_prof_performance = {}

    depart = {"N": {"B_win": 0, "N_win": 0, "draw": 0, "total": 0}, 
              "B": {"B_win": 0, "N_win": 0, "draw": 0, "total": 0}}

    for p in parties:
        lignes = p.strip().split('\n')
        if len(lignes) < 6: continue

        ia_b = lignes[0].split(' VS ')[0].replace('(B)', '').strip()
        ia_n = lignes[0].split(' VS ')[1].replace('(N)', '').strip()
        h_b = lignes[1].split(' VS ')[0].replace('(B)', '').strip()
        h_n = lignes[1].split(' VS ')[1].replace('(N)', '').strip()

        ia_matchs_count[ia_b] = ia_matchs_count.get(ia_b, 0) + 1
        ia_matchs_count[ia_n] = ia_matchs_count.get(ia_n, 0) + 1

        sb, sn, pb, pn, qui_commence = 0, 0, "None", "None", ""
        pre_b, pre_n = "None", "None"

        for l in lignes:
            if "Score du joueur B" in l: sb = int(l.split(':')[-1].strip())
            if "Score du joueur N" in l: sn = int(l.split(':')[-1].strip())
            if "Profondeur Blanc" in l: pb = l.split(':')[-1].strip()
            if "Profondeur Noir" in l: pn = l.split(':')[-1].strip()
            if "commence" in l: qui_commence = l.split(' ')[0].strip()

            # Gestion générale du préprocesseur, Blanc ou Noir
            if "Preprocessor" in l:
                if "Blanc" in l: pre_b = l.split(':')[1].strip()
                if "Noir" in l: pre_n = l.split(':')[1].strip()
            
            if "Temps moyen" in l:
                curr_ia = ia_b if "Blanc" in l else ia_n
                curr_prof = pb if "Blanc" in l else pn
                tps = float(l.split(':')[-1].split('sec')[0].strip())
                ia_temps_total[curr_ia] = ia_temps_total.get(curr_ia, 0) + tps
                ia_coups_total[curr_ia] = ia_coups_total.get(curr_ia, 0) + 1
                
                key = (curr_ia, curr_prof)
                if key not in ia_prof_performance: ia_prof_performance[key] = [0, 0, 0]
                ia_prof_performance[key][1] += tps
                ia_prof_performance[key][2] += 1
            
            if "NumberOfNodes:" in l:
                curr_ia = ia_b if "White" in l else ia_n
                curr_prof = pb if "White" in l else pn
                nb_n = int(l.split(':')[-1].strip())
                ia_noeuds_total[curr_ia] = ia_noeuds_total.get(curr_ia, 0) + nb_n
                
                key = (curr_ia, curr_prof)
                if key not in ia_prof_performance: ia_prof_performance[key] = [0, 0, 0]
                ia_prof_performance[key][0] += nb_n


        win_b, win_n, nul = sb > sn, sn > sb, sb == sn
        if win_b and sn == 0: perfects[ia_b] = perfects.get(ia_b, 0) + 1
        if win_n and sb == 0: perfects[ia_n] = perfects.get(ia_n, 0) + 1

        # Mise à jour des stats brutes et heuristiques
        maj(stats_ia_brutes, ia_b, win_b, nul)
        maj(stats_ia_brutes, ia_n, win_n, nul)
        maj(stats_heuristiques, h_b, win_b, nul)
        maj(stats_heuristiques, h_n, win_n, nul)
        
        if ia_b not in ia_heuristiques: ia_heuristiques[ia_b] = {}
        if ia_n not in ia_heuristiques: ia_heuristiques[ia_n] = {}
        maj(ia_heuristiques[ia_b], f"{h_b} | {pre_b}", win_b, nul)
        maj(ia_heuristiques[ia_n], f"{h_n} | {pre_n}", win_n, nul)

        if pb != "None": maj(stats_profondeur, pb, win_b, nul)
        if pn != "None": maj(stats_profondeur, pn, win_n, nul)
        
        maj(configs, (ia_b, h_b, pb, pre_b), win_b, nul)
        maj(configs, (ia_n, h_n, pn, pre_n), win_n, nul)

        if ia_b != ia_n:
            for att, defen, vic in [(ia_b, ia_n, win_b), (ia_n, ia_b, win_n)]:
                if att not in nemesis: nemesis[att] = {}
                maj(nemesis[att], defen, vic, nul)

        for ia, score, adv, win in [(ia_b, sb, sn, win_b), (ia_n, sn, sb, win_n)]:
            ecart = score - adv
            if ia not in ecarts: 
                ecarts[ia], pions_totaux[ia] = 0, 0
                victoires_data[ia], defaites_data[ia] = [0, 0], [0, 0]
            ecarts[ia] += ecart
            pions_totaux[ia] += score
            if win:
                victoires_data[ia][0] += 1; victoires_data[ia][1] += ecart
            elif score < adv:
                defaites_data[ia][0] += 1; defaites_data[ia][1] += ecart
        
        if qui_commence in depart:
            depart[qui_commence]["total"] += 1
            if nul: depart[qui_commence]["draw"] += 1
            elif win_b: depart[qui_commence]["B_win"] += 1
            elif win_n: depart[qui_commence]["N_win"] += 1
    #Partie ou on va écrire
    out = open('analyse.txt', 'w', encoding='utf-8')
    out.write("==================================================\n")
    out.write("         BILAN STATISTIQUE COMPLET DES IA\n")
    out.write("==================================================\n\n")

    tri_ia = sorted(stats_ia_brutes, key=lambda x: (stats_ia_brutes[x][0] + 0.5*stats_ia_brutes[x][1])/stats_ia_brutes[x][2], reverse=True)

    # 1. Performance Brute (avec Noeuds/Partie et Noeuds/Coup)
    out.write("1. PERFORMANCE BRUTE DES ALGORITHMES\n")
    for ia in tri_ia:
        v, n, t = stats_ia_brutes[ia]
        wr = (v + 0.5*n) / t * 100
        tps = ia_temps_total.get(ia, 0) / ia_coups_total.get(ia, 1)
        nps = ia_noeuds_total.get(ia, 0) / ia_temps_total.get(ia, 0.0001)
        npm = ia_noeuds_total.get(ia, 0) / ia_matchs_count.get(ia, 1) 
        npc = ia_noeuds_total.get(ia, 0) / ia_coups_total.get(ia, 1) 
        out.write(f"- {ia:20} : {wr:5.1f}% WR | {v}V, {n}N sur {t}\n")
        out.write(f"    > Noeuds/partie: {npm:,.0f} | Noeuds/coup: {npc:,.0f}\n")
        out.write(f"    > Temps moy: {tps:.4f}s | Débit: {nps:,.0f} n/s\n")

    out.write("\n2. IMPACT REEL DE LA PROFONDEUR\n")
    for pr in sorted(stats_profondeur.keys()):
        v, n, t = stats_profondeur[pr]
        out.write(f"- Profondeur {pr} : {(v+0.5*n)/t*100:5.1f}% de réussite globale\n")

    out.write("\n3. ANALYSE DES HEURISTIQUES (GLOBAL)\n")
    for h in sorted(stats_heuristiques, key=lambda x: (stats_heuristiques[x][0]+0.5*stats_heuristiques[x][1])/stats_heuristiques[x][2], reverse=True):
        v, n, t = stats_heuristiques[h]
        out.write(f"- {h:25} : {(v+0.5*n)/t*100:5.1f}% de winrate\n")

    out.write("\n4. TOP 5 DES MEILLEURES COMBINAISONS (IA + SCORE + PROF/TYPE)\n")
    top_5 = sorted(configs.items(), key=lambda x: (x[1][0]+0.5*x[1][1])/x[1][2], reverse=True)[:5]
    for i, (cfg, res) in enumerate(top_5, 1):
        v, n, t = res
        # Si BetterMontecarlo, afficher le type (préprocesseur) à la place de Prof
        prof_or_type = cfg[3] if "BetterMontecarlo" in cfg[0] else cfg[2]
        out.write(f"{i}. {cfg[0]} ({cfg[1]}, {prof_or_type}) -> {(v+0.5*n)/t*100:.1f}% ({v}V/{t})\n")


    out.write("\n5. DOMINATION ET STATISTIQUES DE PIONS\n")
    for ia in tri_ia:
        t = stats_ia_brutes[ia][2]
        v_nb, v_somme = victoires_data[ia]
        d_nb, d_somme = defaites_data[ia]
        out.write(f"- {ia:20} : Ecart global {ecarts[ia]/t:+.1f}\n")
        out.write(f"    > Moy. en Victoire: +{v_somme/v_nb if v_nb>0 else 0:.1f} | Moy. en Défaite: {d_somme/d_nb if d_nb>0 else 0:.1f}\n")
        out.write(f"    > Pions moy: {pions_totaux[ia]/t:.1f} | Perfects: {perfects.get(ia, 0)}\n")

    out.write("\n6. CLASSEMENT DES CONFRONTATIONS (MATRICE NEMESIS)\n")
    for ia in tri_ia:
        advs = nemesis.get(ia, {})
        if not advs: continue
        out.write(f"- {ia:20} :\n")
        sorted_advs = sorted(advs.keys(), key=lambda x: (advs[x][0] + 0.5*advs[x][1])/advs[x][2], reverse=True)
        for adv_name in sorted_advs:
            v_n, n_n, t_n = advs[adv_name]
            wr_n = (v_n + 0.5*n_n) / t_n * 100
            out.write(f"    > vs {adv_name:20} : {wr_n:5.1f}% WR ({v_n}V/{t_n})\n")

    out.write("\n7. PERFORMANCE DES HEURISTIQUES PAR ALGORITHME\n")
    for ia in tri_ia:
        out.write(f"- {ia}:\n")
        for h in sorted(ia_heuristiques.get(ia, {}).keys()):
            v, n, t = ia_heuristiques[ia][h]
            out.write(f"    > {h:25} : {(v+0.5*n)/t*100:5.1f}% WR ({v}V/{t})\n")

    out.write("\n8. ANALYSE DU TOUR DE DEPART\n")
    for q in ["N", "B"]:
        tot = depart[q]["total"]
        if tot > 0:
            out.write(f"Matchs commençant par {q} ({tot} parties) :\n")
            out.write(f"  > Victoires Noirs (N) : {depart[q]['N_win']/tot*100:4.1f}%\n")
            out.write(f"  > Victoires Blancs (B) : {depart[q]['B_win']/tot*100:4.1f}%\n")

    out.write("\n9. RÉPARTITION TECHNIQUE PAR ÉTAGE DE PROFONDEUR\n")
    for ia in tri_ia:
        if ia in ia_depth_details:
            out.write(f"- {ia}:\n")
            for p_match in sorted(ia_depth_details[ia].keys()):
                out.write(f"    [Config Profondeur {p_match}]\n")
                for etage in sorted(ia_depth_details[ia][p_match].keys()):
                    somme, nb = ia_depth_details[ia][p_match][etage]
                    out.write(f"      > Niveau {etage} : {somme/nb:,.1f} noeuds générés en moyenne\n")

    out.write("\n10. ANALYSE CROISÉE IA / PROFONDEUR (EFFORT DE CALCUL)\n")
    for key in sorted(ia_prof_performance.keys()):
        ia_n, prof_n = key
        n_tot, t_tot, c_tot = ia_prof_performance[key]
        out.write(f"- {ia_n:15} (Prof {prof_n:4}) : {t_tot/c_tot:.4f}s/coup | {n_tot/c_tot:,.0f} noeuds/parties\n")

    # --- Section 11 Classement total ---
    out.write("\n11. CLASSEMENT TOTAL DES CONFIGURATIONS (DE LA PLUS FORTE A LA PLUS NULLE)\n")
    toutes_configs = sorted(configs.items(), key=lambda x: (x[1][0]+0.5*x[1][1])/x[1][2], reverse=True)
    for i, (cfg, res) in enumerate(toutes_configs, 1):
        v, n, t = res
        wr = (v + 0.5*n) / t * 100
        prof_or_type = cfg[3] if "BetterMontecarlo" in cfg[0] else cfg[2]
        out.write(f"{i:2}. {cfg[0]:25} | {cfg[1]:25} | {prof_or_type:10} : {wr:5.1f}% ({v}V/{t})\n")


    # --- Section 12 : comparaison FSP vs VSP uniquement pour BetterMontecarlo ---
    out.write("\n12. COMPARAISON DES PREPROCESSORS (FSP vs VSP)\n")
    for ia in ia_heuristiques:
        if "BetterMontecarlo" not in ia:  # ne traiter que BetterMontecarlo
            continue
        fsp_stats = [0, 0, 0]
        vsp_stats = [0, 0, 0]
        for key in ia_heuristiques[ia]:
            if "FSP" in key: 
                fsp_stats = ia_heuristiques[ia][key]
            if "VSP" in key: 
                vsp_stats = ia_heuristiques[ia][key]
        fsp_wr = (fsp_stats[0] + 0.5*fsp_stats[1]) / (fsp_stats[2] if fsp_stats[2]>0 else 1) * 100
        vsp_wr = (vsp_stats[0] + 0.5*vsp_stats[1]) / (vsp_stats[2] if vsp_stats[2]>0 else 1) * 100
        meilleur = "FSP" if fsp_wr > vsp_wr else "VSP" if vsp_wr > fsp_wr else "Egalité"
        out.write(f"- {ia:25} : FSP WR={fsp_wr:.1f}%, VSP WR={vsp_wr:.1f}% -> Meilleur: {meilleur}\n")
        out.close()

    print("Analyse complète et classement total générés.")

analyse_finale_ia()