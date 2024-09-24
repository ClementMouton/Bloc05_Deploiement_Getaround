# Bloc05_Deploiement_Getaround

GetAround est l'Airbnb des voitures. Vous pouvez louer des voitures à n’importe qui pour quelques heures à quelques jours ! Fondée en 2009, cette entreprise a connu une croissance rapide. En 2019, ils comptent plus de 5 millions d'utilisateurs et environ 20 000 voitures disponibles dans le monde.

En tant que partenaire de Jedha, ils ont proposé de grands défis :

# Contexte

Lors de la location d'une voiture, nos utilisateurs doivent effectuer un flux d'enregistrement au début de la location et un flux de paiement à la fin de la location afin de :

Évaluez l’état de la voiture et informez les autres parties des dommages préexistants ou survenus pendant la location. Comparez les niveaux de carburant. Mesurez combien de kilomètres ont été parcourus. Le check-in et le check-out de nos locations peuvent se faire avec trois flux distincts :

📱 Contrat de location mobile sur applications natives : chauffeur et propriétaire se rencontrent et signent tous deux le contrat de location sur le smartphone du propriétaire Connect : le conducteur ne rencontre pas le propriétaire et ouvre la voiture avec son smartphone 📝 Contrat papier (négligeable)

# Projet 🚧

Pour cette étude de cas, nous vous proposons de vous mettre à notre place et de réaliser une analyse que nous avons réalisée en 2017 🔮 🪄

Lorsqu'ils utilisent Getaround, les conducteurs réservent des voitures pour une période spécifique, allant d'une heure à quelques jours. Ils sont censés ramener la voiture à temps, mais il arrive de temps en temps que les chauffeurs soient en retard au passage en caisse.

Les retours tardifs à la caisse peuvent générer de fortes frictions pour le conducteur suivant si la voiture était censée être louée à nouveau le même jour : le service client signale souvent des utilisateurs insatisfaits car ils ont dû attendre que la voiture revienne de la location précédente ou des utilisateurs qui ils ont même dû annuler leur location car la voiture n'était pas restituée à temps.

# Objectifs 🎯

Afin d'atténuer ces problèmes, nous avons décidé de mettre en place un délai minimum entre deux locations. Une voiture ne sera pas affichée dans les résultats de recherche si les heures d'arrivée ou de départ demandées sont trop proches d'une location déjà réservée.

Cela résout le problème des départs tardifs, mais peut également nuire aux revenus de Getaround et des propriétaires : nous devons trouver le bon compromis.

Notre chef de produit doit encore décider :

seuil : quelle doit être la durée du délai minimum ? portée : devrions-nous activer la fonctionnalité pour toutes les voitures ?, uniquement pour les voitures Connect ? Afin de les aider à prendre la bonne décision, ils vous demandent des informations sur les données. Voici les premières analyses auxquelles ils ont pu penser, pour relancer la discussion. N'hésitez pas à effectuer des analyses complémentaires que vous jugerez pertinentes.

Quelle part des revenus de notre propriétaire serait potentiellement affectée par cette fonctionnalité ? Combien de locations seraient concernées par cette fonctionnalité, en fonction du seuil et de la portée que nous choisissons ? À quelle fréquence les conducteurs sont-ils en retard au prochain enregistrement ? Quel impact cela a-t-il sur le prochain conducteur ? Combien de cas problématiques résoudra-t-il en fonction du seuil et de la portée choisis ?
