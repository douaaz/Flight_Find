$(document).ready(function(){
    $("button").click(function (event) {
        var info = eval(results);
        var data = {
            "from" : $('#all_from').val(),
            "to" : $('#all_to').val(),
            "airline_name" : $('#airline_name').val(),
            "flight_num" : $('#flight_num').val(),
            "start_date" : $('#all_start_date').val(),
            "end_date" : $('#all_end_date').val(),
            "status" : $('#status').val()
        };

        if (data){
            /*from 过滤*/
            if (data["from"] != '' && data["from"] != 'any'){
                var temp = new Array();
                for (var i = 0; i< info.length; i++){
                    if (info[i].departure_airport == data["from"]){
                        temp.push(info[i]);
                        };
                }
                var info = temp;
            }

            /*to 过滤*/
            if (data["to"] != '' && data["to"] != 'any'){
                var temp = new Array();
                for (var i = 0; i< info.length;i++){
                    if (info[i].arrival_airport == data["to"]){
                        temp.push(info[i]);
                        }
                }
                var info = temp;
            }

            /*flight_num 过滤*/
            if (data["flight_num"] != '' && data["flight_num"] != 'any'){
                var temp = new Array();
                for (var i = 0; i< info.length;i++){
                    if (info[i].flight_num == data["flight_num"]){
                        temp.push(info[i]);
                        }
                }
                var info = temp;
            }

            /*start_date 过滤*/
            if (data["start_date"] != '' && data["start_date"] != 'any'){
                var temp = new Array();
                var htmlcomp = data["start_date"].split('-');
                var start_date = new Date(htmlcomp.join('/'));
                for (var i = 0; i < info.length; i++){
                    console.log(info.length);
                    var dbcomp = info[i].departure_time.split(' ')[0];
                    dbcomp = dbcomp.split('-');
                    var data_date = new Date(dbcomp.join('/')) ;
                    console.log(data_date);
                    if (data_date >= start_date){
                        temp.push(info[i]);
                        }
                }
                info = temp;
            }


            /*end_date 过滤*/
            if (data["end_date"] != '' && data["end_date"] != 'any'){
                var temp = new Array();
                for (var i = 0; i< info.length; i++){
                    var htmlcomp2 = data["end_date"].split('-');
                    var end_date = new Date(htmlcomp2.join('/'));
                    var dbcomp2 = info[i].departure_time.split(' ')[0];
                    dbcomp2 = dbcomp2.split('-');
                    var data_date = new Date(dbcomp2.join('/')) ;
                    if (data_date <= end_date){
                        temp.push(info[i]);
                        }
                }
                info = temp;
            }
            /*status 过滤*/
            if (data["status"]){
                var temp = new Array();
                for (var i = 0; i< info.length;i++){
                    if (info[i].status == data["status"]){
                        console.log("IN!!!!")
                        temp.push(info[i]);
                        }
                }
                info = temp;

            }
            console.log(info);
            /*clear previous search result*/
            document.getElementById("result").innerHTML = '';
            for (var i = 0; i < info.length; i++){

                var airline_name = document.createElement('li');
                    airline_name.innerHTML = info[i]["airline_name"];
                var flight_num = document.createElement('li');
                    flight_num.innerHTML = info[i]["flight_num"];
                var depature_ap = document.createElement('li');
                    depature_ap.innerHTML = info[i]["departure_airport"];
                var departure_time = document.createElement('li');
                    departure_time.innerHTML = info[i]["departure_time"];
                var arrival_ap = document.createElement('li');
                    arrival_ap.innerHTML = info[i]["arrival_airport"];
                var arrival_time = document.createElement('li');
                    arrival_time.innerHTML = info[i]["arrival_time"];
                var price = document.createElement('li');
                    price.innerHTML = info[i]["price"];
                var status = document.createElement('li');
                    status.innerHTML = info[i]["status"];
                var customer = document.createElement('li');
                    customer.innerHTML = info[i]["customer_email"];


                document.getElementById("result").appendChild(airline_name);
                document.getElementById("result").appendChild(flight_num);
                document.getElementById("result").appendChild(depature_ap);
                document.getElementById("result").appendChild(departure_time);
                document.getElementById("result").appendChild(arrival_ap);
                document.getElementById("result").appendChild(arrival_time);
                document.getElementById("result").appendChild(price);
                document.getElementById("result").appendChild(status);
                document.getElementById("result").appendChild(customer);

            }
        }
    });
});