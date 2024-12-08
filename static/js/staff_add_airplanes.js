$(document).ready(function () {
    $('#add_airplane_form').on('submit', function (event) {
        $.ajax({
            data:{
                airline_name : $('#airline_name').val(),
                airplane_id : $('#airplane_id').val(),
                seats : $('#seats').val(),
            },
            type : 'POST',
            url : '/staffAddAirplane'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]) {
                console.log("IN!!!");
                /*clean previous search results:*/
                document.getElementById('airplane_search').innerHTML = '';
                let listdata = data["data"];
                /*column creation*/
                title = document.createElement('p');
                title.innerHTML = listdata;
                /*put <li> onto <div>*/
                document.getElementById('airplane_search').appendChild(title);
            }

            else {
                /*clean previous data*/
                document.getElementById('airport_search').innerHTML = '';
                var li = document.createElement('li');
                li.innerHTML = data["data"];
                document.getElementById("airport_search").appendChild(li);
            }
        });
        event.preventDefault();
    });

});

