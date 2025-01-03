$(document).ready(function () {
    $('#form').on('submit', function (event) {
        $.ajax({
            data:{
                customer_email : $('#cust_email').val(),
            },
            type : 'POST',
            url : '/staffProcessCustomers'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                console.log(data["data"]);
                /*clean previous search results:*/
                document.getElementById('result').innerHTML = '';
                let info = eval(data["data"]);
                for (var i = 0; i < info.length; i++){
                    var flight_num = document.createElement('li');
                        flight_num.innerHTML = info[i][1];
                    var depature_ap = document.createElement('li');
                        depature_ap.innerHTML = info[i][2];
                    var departure_time = document.createElement('li');
                        departure_time.innerHTML = info[i][3];
                    var arrival_ap = document.createElement('li');
                        arrival_ap.innerHTML = info[i][4];
                    var arrival_time = document.createElement('li');
                        arrival_time.innerHTML = info[i][5];

                    document.getElementById("result").appendChild(flight_num);
                    document.getElementById("result").appendChild(depature_ap);
                    document.getElementById("result").appendChild(departure_time);
                    document.getElementById("result").appendChild(arrival_ap);
                    document.getElementById("result").appendChild(arrival_time);
            }

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