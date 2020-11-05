function createBlock(message, side) {
    if (side === 'right') {
        typeBlock = 'block-sendedMessage'
    } else if (side === 'left') {
        typeBlock = 'block-receivedMessage'
    }
    
    $('#textbox-messageschat').append("<p class='block " + typeBlock + "'>" + message + "</p>")
}


let socket = io.connect('http://' + document.domain + ':' + location.port)


socket.on('connect', function() {
    joining()
    sendMessage()
    back()
})


function joining() {
    socket.emit('joining')
}


function sendMessage() {
    let send = $('#button-form_send').on('click', function(event) {
        event.preventDefault()

        let message = $('#textbox-form_message').val()
        $('#textbox-form_message').val('')

        createBlock(message, 'right')

        socket.emit('chating', message)
    })
}


function back() {
    $('#button-back').on('click', function(event) {
        event.preventDefault()
        socket.emit('disconnect')
        location.replace('http://' + document.domain + ':' + location.port + '/')
    })
}


socket.on('chating', function(message) {
    createBlock(message, 'left')
})
