// variables pour le toggle du chat :
// variables pour le toggle du chat :
const popup = document.querySelector(".chat-popup");
const chatBtn = document.querySelector(".chat-btn");
// variable pour l'envoi de messages :
const submitBtn = document.querySelector(".submit");
// Zone de chat, zone d'input et contenu d'input :
const chatArea = document.querySelector(".chat-area");
const inputElm = document.querySelector("input");
const inputArea = document.querySelector(".input-area");
// variables pour le système d'emojis :
const emojiBtn = document.querySelector('#emoji-btn');
const picker = new EmojiButton();



const animateCSS = (element, animation, prefix = 'animate__') =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = document.querySelector(element);

    node.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
      event.stopPropagation();
      node.classList.remove(`${prefix}animated`, animationName);
      resolve('Animation ended');
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
  });



// INFO :
// Ce type de structures : () => {}
// correspond à des arrow functions ES6
// Il s'agit de fonctions js à la syntaxe simplifiée
// "()" veut dire que la fonction fléchée est anonyme

// Sélection d'Emojis : 
picker.on('emoji', selectedEmoji => {
    // On ajoute l'emoji choisi à l'input de la zone de saisie
    document.querySelector('input').value += selectedEmoji;
});

emojiBtn.addEventListener('click', () => {
    // On affiche le sélecteur d'emoji quand l'utilisateur clique sur le bouton
    picker.togglePicker(emojiBtn);
});

// Affichage du chat avec le bouton :
chatBtn.addEventListener('click', ()=>{

    if (popup.classList.contains('show')) // Si la classe show est présente dans les classes de l'élément popup
        {
            $('.popup-icon').html('live_help')
            animateCSS(element='.chat-btn', 'rubberBand')
            // Do something after the animation
            animateCSS(element='.chat-popup', 'fadeOutDown').then((message) => {
                popup.classList.toggle('show', force=false)
                autoFocus();
              });
        }

    else
    {

        animateCSS(element='.chat-btn', 'rubberBand')
        $('.popup-icon').html('close')
        // Do something after the animation
        popup.classList.toggle('show', force=true)
        autoFocus();
        scrollToBottom();
        animateCSS(element='.chat-popup', 'fadeInUp').then((message) => {})

    }

})
/**
 * Envoi d'un message via la zone d'input
 * Le message de l'utilisateur est envoyé à l'API via ajax, il y est traité et la réponse 
 * du chatbot est renvoyée une fois que le modèle a prédit. En attendant la réponse du bot,
 * une réponse temporaire faite de trois petits points animée est affichée.
 */
function sendMessage(){
    //
    let userInput = inputElm.value;
    console.log(userInput)

    if (userInput.length == 0) // si la zone de saisie est vide
        {
            // on envoie rien
        }
    else
        {
            // On crée un élément html correspondant au message écrit par l'utilisateur 
            let temp = `<div class="out-msg animate__animated animate__zoomIn">
            <span class="my-msg">${userInput}</span>
            <img src=${avatarUser} class="avatar">
            </div>`;

            // on récupère le modèle sur l'API :
            const modelURL = 'http://localhost:5000/chatbot/model';

            // On crée une fonction pour récupérer la réponse du chatbot via le modèle
            async function loadModel(reponse) {
                let temp = `<div class="income-msg is-typing animate__animated animate__zoomIn">
                <img class="avatar" src="${avatarBot}" alt="avatar du chatbot">
                <span class="msg">
                <p class="loading"><span>.</span><span>.</span><span>.</span></p>
                </span>
                </div>`
                chatArea.insertAdjacentHTML("beforeend", temp)
                scrollToBottom()

                reponse = tf.tensor(reponse);
                console.log(reponse.dataSync());
                // const model = await tf.loadGraphModel(modelURL);
                const model = await tf.loadLayersModel(modelURL);
                console.log('Modèle Chargé')

                // let prediction = await model.executeAsync(reponse)
                let prediction = model.predict(reponse);
                let label = prediction.argMax(axis = 1).dataSync()[0];
                console.log('Prédiction :', label);

                let probabilities = tf.softmax(prediction).dataSync()[label];
                console.log('Proba Label :', probabilities);
                // console.log('Proba_max :', tf.argMax(probabilities).dataSync()[0]);
                // Quand la prediction est juste cela descend rarement de dessous de 0,020/0,022

                $.ajax({
                    url:"/get_tag", 
                    data: {jsdata: label}, 
                    type:"POST", 
                    dataType : 'json',
                    success: function(reponse){

                        $('.is-typing').remove();

                        if (probabilities < 0.018 || reponse == ''){
                            reponse = "Je n'ai pas bien compris la demande, pouvez-vous reformuler ?";
                        }
                        let temp = `<div class="income-msg">
                                    <img class="avatar animate__animated animate__fadeInLeft" src="${avatarBot}" alt="avatar du chatbot">
                                    <span class="msg animate__animated animate__zoomIn">
                                    ${reponse}
                                    </span>
                                    </div>`

                        chatArea.insertAdjacentHTML("beforeend", temp)
                        scrollToBottom();
                    }
                })
            }

            $.ajax({
                url:"/pretreatment", 
                data: {jsdata: userInput}, 
                type:"POST", 
                dataType : 'json', 
                success: function(reponse){
                    loadModel(reponse);
                }
            })
            chatArea.insertAdjacentHTML("beforeend", temp);
            scrollToBottom();
            inputElm.value=""; //vidage de la zone de saisie après envoi        
        }
}

// Envoi de messages au chat :
// 1er cas, écoute du clic :
submitBtn.addEventListener('click', ()=>{
    sendMessage();
    scrollToBottom();
})
// 2ème cas, écoute de la touche entrée :
inputArea.addEventListener("keyup", ({key}) => {
    // On vérifie que la variable key passée dans la fonction
    // fléchée du listener correspond à la touche entrée :
    if (key === "Enter") {
        sendMessage();
        scrollToBottom();
    }
})



// Lignes de commandes pour convertir le modèle, laissées pour rappel.
// tensorflowjs_converter --input_format=keras --output_format=tfjs_layers_model ./chemin_vers_le_model/model.h5 ./nom_dossier_ou_enregistrer_le_model_js

// tensorflowjs_converter --input_format=tf_saved_model ./model_keras/model_3 ./model_3_js


/**
 * Défilement automatique vers le bas du chat 
 * (fonction appelée en cas de nouveauxmessages).
 */
function scrollToBottom() {
    chatArea.scrollTop = chatArea.scrollHeight;
    // scrollHeight est la hauteur totale du contenu, scrollTop le nombre de pixels défilés,
    // équivaloir les deux nous amène tout en bas du contenu
  }

/**
 * Focus sur la zone de saisie quand on ouvre le chat,
 * pour éviter à l'utilisateur de devoir cliquer dedans
 */
function autoFocus() {
    inputElm.focus();
}


// En cas de refresh/nouvelle visite de la page, réinjection dans la popup de l'historique de chat s'il existe :
reinjection_messages(messages = historique)

/**
 * Cette fonction réinjecte dans le chat les messages de l'historique stocké en session.
 * Elle prend en paramètre les messages qui viennent au js via une injection de variable
 * jinja2 dans le index.html.
 * @param {*} messages 
 */
function reinjection_messages(messages){
    console.log(typeof(messages[0]))
    messages.forEach(function (element, index){
        console.log(element, index)
        if (element[1] == "chatbot"){

            let temp = `<div class="income-msg">
            <img class="avatar" src="${avatarBot}" alt="avatar du chatbot">
            <span class="msg">
            ${element[2]}
            </span>
            </div>`
            chatArea.insertAdjacentHTML("beforeend", temp); // Ajout du message à la fin des messages existants
        }

        else {
            let temp = `<div class="out-msg">
            <span class="my-msg">
            ${element[2]}
            </span>
            <img class="avatar" src="${avatarUser}" alt="avatar de l'utilisateur">
            </div>`
            chatArea.insertAdjacentHTML("beforeend", temp); // Ajout du message à la fin des messages existants
        }

    });
}