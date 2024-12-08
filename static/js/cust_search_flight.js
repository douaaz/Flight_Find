$(document).ready(function () {
    $('#searchform').on('submit', function (event) {
        $.ajax({
            data:{
                from : $('#all_from').val(),
                to : $('#all_to').val(),
                date : $('#all_date').val(),
            },
            type : 'POST',
            url : '/customerSearchFlight'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                console.log("IN!!!");
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
                /*create <ul>*/
                var ul = document.createElement('ul');
                document.getElementById('result').appendChild(ul);

                console.log(ul);
                /*sql data handling*/
                for (var i = 0; i < listdata.length; i++ ){
                    var li = document.createElement('li');
                    //the data format Don't forget to delete that 1!!!
                    for (var j = 0; j < listdata[i].length-1; j++){
                        var li2 = document.createElement('li');
                        li2.innerHTML = listdata[i][j];
                        console.log(li2);
                        li.appendChild(li2);

                    }

                    //write sold out on the last column
                    if (listdata[i][8] == 1){
                        var sold_out = document.createElement('li');
                        sold_out.innerHTML = "Sold Out";
                        li.appendChild(sold_out);
                    }
                    else {
                        // create form after every flight
                        var form_li = document.createElement('li');
                        var form = document.createElement('form');
                        var input_airline_name = document.createElement('input');
                            input_airline_name.classList.add("class1");
                        var input_flight_num = document.createElement('input');
                            input_flight_num.classList.add("class1");
                        var button = document.createElement('button');

                        form.action = "/customerPurchaseDetail";
                        form.method = "post";
                        input_airline_name.type = "text";
                        input_airline_name.name = "airline_name";
                        input_airline_name.value = listdata[i][0];
                        input_flight_num.type = "text";
                        input_flight_num.name = "flight_num";
                        input_flight_num.value = listdata[i][1];
                        button.innerHTML = "Purchase";
                        form.appendChild(input_airline_name);
                        form.appendChild(input_flight_num);
                        form.appendChild(button);
                        form_li.appendChild(form);
                        li.appendChild(form_li);
                    }
                    ul.appendChild(li);

                }
                console.log(ul);
            }
            else {
                /*clean previous data*/
                document.getElementById('result').innerHTML = '';
                li = document.createElement('li');
                li.innerHTML = data["error"];
                document.getElementById("result").appendChild(li);

            }
        });
        event.preventDefault();
    });

});

