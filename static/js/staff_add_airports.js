$(document).ready(function () {
    $('#add_airport_form').on('submit', function (event) {
        $.ajax({
            data:{
                airport_name : $('#airport_name').val(),
                airport_city : $('#airport_city').val(),
            },
            type : 'POST',
            url : '/staffAddAirport'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]) {
                console.log("IN!!!");
                /*clean previous search results:*/
                document.getElementById('airport_search').innerHTML = '';
                let listdata = data["data"];
                /*column creation*/
                title = document.createElement('p');
                title.innerHTML = listdata;
                /*put <li> onto <div>*/
                document.getElementById('airport_search').appendChild(title);
            }

            else {
                /*clean previous data*/
                document.getElementById('airport_search').innerHTML = '';
                var li = document.createElement('li');
                li.innerHTML = data["error"];
                document.getElementById("airport_search").appendChild(li);
            }
        });
        event.preventDefault();
    });

});

