let socket = io.connect('http://' + document.domain + ':' + location.port)

socket.on('connect', function() {
    getUser()
    getResponce()
})

function getUser() {
    let form = $('form').on('submit', function(event) {
        event.preventDefault()

        let username = $('#form_input').val()

        socket.emit('getuser', {
            username: username
        })
    })
}

function getResponce() {
    socket.on('getuser', function(responce) {
        if (responce === 'redirect') {
            location.replace('http://' + document.domain + ':' + location.port + '/chat')
        } else if (responce === 'wait') {
            $('#responce').text('Wait, the user has not yet connected to you.')
        } else if (responce === 'notfound') {
            $('#responce').text('The user with the given name does not exist.')
        } else if (responce === 'occupied') {
            $('#responce').text('The user is currently chatting with another user.')
        }
    })
}