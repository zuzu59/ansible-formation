# Remote debugging

1. préparer l’egg : installer PyCharm ou IntelliJ avec le plug-in Python; trouver le fichier pycharm.egg dans les dossiers du répertoire personnel pour ce plug-in; l’unzipper quelque part. <br>💡 <pre>find ~ -name "*pycharm.egg"</pre>
2. Patcher l’image : https://dpaste.com/4PHETBDEA puis cataiamsible -t sativa
3. Configurer et lancer IntelliJ avec une session de débogueur Python à distance
4. Lancer un tunnel, par exemple avec [ngrok.io](https://ngrok.io), vers localhost port 12477 (ou quoi que ce soit que vous avez configuré dans IntelliJ)<pre>ngrok tcp 12477</pre>💡 nécessite d’installer ngrok, puis à la première utilisation, de se connecter à ngrok.io puis s’authentifier en ligne de commande avec un token.
5. Créer les fichiers /tmp/DEBUG-HOST et /tmp/DEBUG-PORT dans le container à l’aide d’`oc exec` ou de la console OKD . ⚠ Attention à ne pas mettre un retour-chariot à la fin !<br>Exemple : <pre>oc -n catalyse-test exec -it $(oc -n catalyse-test get pod -o name|grep sativa|grep -v deploy |cut -d/ -f2) -- bash -c "echo -n 6.tcp.ngrok.io > /tmp/DEBUG-HOST"
oc -n catalyse-test exec -it $(oc -n catalyse-test get pod -o name|grep sativa|grep -v deploy |cut -d/ -f2) -- bash -c "echo -n 13537 > /tmp/DEBUG-PORT"
</pre>
6. Envoyer l’egg : depuis le répertoire de l’étape ①,<pre>tar -clf - . | oc -n catalyse-test exec -i $(oc -n catalyse-test get pod -o name|grep sativa|grep -v deploy |cut -d/ -f2) -- bash -c 'cd /opt/satosa/etc; tar -xpvf -'</pre>
7.  ???
8. Profit!
