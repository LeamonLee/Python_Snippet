$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5002');

    var socket_namespace1 = io('http://127.0.0.1:5002/namespace1', {rememberTransport: false})

    socket.on('connect_response', function(msg) {
        alert(msg);
    });

    socket.on('message', function(msg) {
        alert(msg);
    });

    socket_namespace1.on('connect_response', function(msg) {
        console.log(msg);
    });

    socket_namespace1.on('message', function(msg) {
        console.log(msg);
    });

    socket_namespace1.on('message2', function(msg) {
        console.log(msg);
    });

    socket_namespace1.on('message3', function(msg) {
        console.log(msg);
    });

    socket_namespace1.on('chatroom_msg', function(msg) {
        console.log(msg);
    });

    $('#default_send').on('click', function() {
        socket.emit('message', "default message");
    });

    $('#namespace1_send').on('click', function() {
        
        socket_namespace1.emit('message', "namespace1 message");
    });

    $('#namespace1_send_msg2').on('click', function() {
        
        socket_namespace1.emit('message2', "namespace1 message2");
    });

    $('#namespace1_send_msg3').on('click', function() {
        
        socket_namespace1.emit('message3', "namespace1 message3");
    });

    $('#namespace1_send_msg4').on('click', function() {
        
        $.ajax({
            type:"GET",
            url:"http://127.0.0.1:5002/websocket/namespace1/message4",
            success:function(msg){
                
                console.log(msg);
            },
            error:function(xhr, ajaxOptions, thrownError){
                console.log(xhr);
                console.log(thrownError);
                
            }
        });
    });

    $('#join_room').on('click', function() {
        
        socket_namespace1.emit('join_room', {username: "Leamon", room: "room1"});
    });

    $('#leave_room').on('click', function() {
        
        socket_namespace1.emit('leave_room', {username: "Leamon", room: "room1"});
    });

    $('#send_msg_room').on('click', function() {
        
        $.ajax({
            type:"GET",
            url:"http://127.0.0.1:5002/websocket/room/room1",
            success:function(msg){
                
                console.log(msg);
            },
            error:function(xhr, ajaxOptions, thrownError){
                console.log(xhr);
                console.log(thrownError);
                
            }
        });
    });
    

    

});