$(document).ready(function () {
    $('form').on('submit', function (event) {
        $.ajax({
            data:{
                from : $('#all_from').val(),
                to : $('#all_to').val(),
                date : $('#all_date').val(),
                flight_num : $('#flight_num').val()
            },
            type : 'POST',
            url : '/publicSearchFlight'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                console.log(data["data"]);
                /*clean previous search results:*/
                document.getElementById('result').innerHTML = '';
                let listdata = data["data"];
                /*column creation*/
                title = document.createElement('p');
                console.log(title);
                /*add list columns*/
                var airline_name = document.createElement('span');
                    airline_name.innerHTML = "Airline Name";
                var flight_num = document.createElement('span');
                    flight_num.innerHTML = "Flight Number";
                var depature_ap = document.createElement('span');
                    depature_ap.innerHTML = "Departure Airport";
                var departure_time = document.createElement('span');
                    departure_time.innerHTML = "Departure Time";
                var arrival_ap = document.createElement('span');
                    arrival_ap.innerHTML = "Arrival Airport";
                var arrival_time = document.createElement('span');
                    arrival_time.innerHTML = "Arrival Time";
                var price = document.createElement('span');
                    price.innerHTML = "Price";
                var status = document.createElement('span');
                    status.innerHTML = "Status";
                /*put <label> onto <li>*/
                title.appendChild(airline_name);
                title.appendChild(flight_num);
                title.appendChild(depature_ap);
                title.appendChild(departure_time);
                title.appendChild(arrival_ap);
                title.appendChild(arrival_time);
                title.appendChild(price);
                title.appendChild(status);

                /*put <li> onto <div>*/
                document.getElementById('result').appendChild(title);
                /*put <ul> onto <div>*/
                ul = document.createElement('ul');
                document.getElementById('result').appendChild(ul);

                console.log(ul);
                /*sql data handling*/
                for (var i = 0; i < listdata.length; i++ ){
                    li = document.createElement('li');
                    // the listdata
                    for (var j = 0; j < listdata[i].length; j++){
                        li2 = document.createElement('li');
                        li2.innerHTML = listdata[i][j];
                        console.log(li2);
                        li.appendChild(li2);
                    }
                    ul.appendChild(li);
                }
                console.log(ul);
            }
            else {
                /*clean previous data*/
                document.getElementById('result').innerHTML = '';
                li = document.createElement('p');
                li.innerHTML = data["error"];
                document.getElementById("result").appendChild(li);

            }
        });
        event.preventDefault();
    });
});