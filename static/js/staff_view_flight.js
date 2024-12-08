$(document).ready(function () {
    var info = eval(results);
    for (var i = 0; i < info.length; i++) {
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
        var form_li = document.createElement("li");
        form_li.style = "border : 0px";

        /*create ajax form to handle change flight operation*/
        var status_change_form = document.createElement('section');
        status_change_form.id = "status_change_form";
        var form_airline_name = document.createElement("input");
        form_airline_name.value = info[i]["airline_name"];
        form_airline_name.type = "text";
        form_airline_name.id = "form_airline_name" + info[i]['flight_num'];
        form_airline_name.classList.add("class1");
        var form_flight_num = document.createElement("input");
        form_flight_num.type = "text";
        form_flight_num.id = "form_flight_num" + info[i]['flight_num'];
        form_flight_num.value = info[i]["flight_num"];
        form_flight_num.classList.add("class1");
        var status = document.createElement("select");
        status.id = "form_status" + info[i]['flight_num'];
        status.value = info[i]["status"];
        var options = ["Upcoming", "In-progress", "Delayed", "Cancelled"];
        var index = options.indexOf(info[i]["status"]);
        options.splice(index, 1);
        options.splice(0, 0, info[i]["status"]);
        for (var j = 0; j < options.length; j++) {
            var option = document.createElement("option");
            option.innerHTML = options[j];
            status.appendChild(option);
        }

        var update = document.createElement("button");
        update.innerHTML = "Update";
        update.type = "submit";
        update.id = info[i]['flight_num'];
        update.classList.add("update_button");
        status_change_form.appendChild(form_airline_name);
        status_change_form.appendChild(form_flight_num);
        status_change_form.appendChild(status);
        status_change_form.appendChild(update);
        form_li.appendChild(status_change_form);

        document.getElementById("result").appendChild(airline_name);
        document.getElementById("result").appendChild(flight_num);
        document.getElementById("result").appendChild(depature_ap);
        document.getElementById("result").appendChild(departure_time);
        document.getElementById("result").appendChild(arrival_ap);
        document.getElementById("result").appendChild(arrival_time);
        document.getElementById("result").appendChild(price);
        document.getElementById("result").appendChild(form_li);
    }

    $("#search").click(function (event) {
        event.preventDefault();
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
                        console.log("IN!!!!");
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
                var form_li = document.createElement("li");
                    form_li.style = "border : 0px";

                /*create ajax form to handle change flight operation*/
                var status_change_form = document.createElement('section');
                    status_change_form.id = "status_change_form";
                var form_airline_name = document.createElement("input");
                    form_airline_name.value = info[i]["airline_name"];
                    form_airline_name.type = "text";
                    form_airline_name.id = "form_airline_name" + info[i]['flight_num'];
                    form_airline_name.classList.add("class1");
                var form_flight_num = document.createElement("input");
                    form_flight_num.type = "text";
                    form_flight_num.id = "form_flight_num" + info[i]['flight_num'];
                    form_flight_num.value = info[i]["flight_num"];
                    form_flight_num.classList.add("class1");
                var status = document.createElement("select");
                    status.id = "form_status" + info[i]['flight_num'];
                    status.value = info[i]["status"];

                var options = ["Upcoming", "In-progress", "Delayed", "Cancelled"];
                var index = options.indexOf(info[i]["status"]);
                options.splice(index, 1);
                options.splice(0, 0, info[i]["status"]);
                for (var j = 0; j < options.length; j++){
                    var option = document.createElement("option");
                    option.innerHTML = options[j];
                    console.log(status);
                    status.appendChild(option);
                }

                var update = document.createElement("button");
                    update.innerHTML = "Update";
                    update.type = "submit";
                    update.id = info[i]['flight_num'];
                    update.classList.add("update_button");
                    status_change_form.appendChild(form_airline_name);
                    status_change_form.appendChild(form_flight_num);
                    status_change_form.appendChild(status);
                    status_change_form.appendChild(update);
                    form_li.appendChild(status_change_form);

                document.getElementById("result").appendChild(airline_name);
                document.getElementById("result").appendChild(flight_num);
                document.getElementById("result").appendChild(depature_ap);
                document.getElementById("result").appendChild(departure_time);
                document.getElementById("result").appendChild(arrival_ap);
                document.getElementById("result").appendChild(arrival_time);
                document.getElementById("result").appendChild(price);
                document.getElementById("result").appendChild(form_li);
            }
        }
    });


    $('.update_button').on("click", function () {
        console.log("HELLO!!!!");
        var button_id = $(this).attr('id');
        console.log($("#form_airline_name"+button_id).val());
        console.log($("#form_status"+button_id).val());
        $.ajax({
            data:{
                airline_name : $("#form_airline_name"+button_id).val(),
                flight_num : button_id,
                status : $("#form_status"+button_id).val()
            },
            type : 'POST',
            url : '/staffChangeFlight'
        })

        .done(function (data) {
            console.log(data);
            if (data["data"]){
                /*
                /!*clear previous search result*!/
                document.getElementById("result").innerHTML = '';

                info = data["data"];
                for (var i = 0; i < info.length; i++) {
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
                    var form_li = document.createElement("li");
                    form_li.style = "border : 0px";

                    /!*create ajax form to handle change flight operation*!/
                    var status_change_form = document.createElement('span');
                        status_change_form.id = "status_change_form";
                    var form_airline_name = document.createElement("input");
                        form_airline_name.value = info[i]["airline_name"];
                        form_airline_name.type = "text";
                        form_airline_name.id = "form_airline_name" + info[i]['flight_num'];
                        form_airline_name.classList.add("class1");
                    var form_flight_num = document.createElement("input");
                        form_flight_num.type = "text";
                        form_flight_num.id = "form_flight_num" + info[i]['flight_num'];
                        form_flight_num.value = info[i]["flight_num"];
                        form_flight_num.classList.add("class1");
                    var status = document.createElement("select");
                        status.id = "form_status" + info[i]['flight_num'];
                        status.value = info[i]["status"];

                    var options = ["Upcoming", "In-progress", "Delayed", "Cancelled"];
                    var index = options.indexOf(info[i]["status"]);
                    options.splice(index, 1);
                    options.splice(0, 0, info[i]["status"]);
                    for (var j = 0; j < options.length; j++){
                        var option = document.createElement("option");
                        option.innerHTML = options[j];
                        status.appendChild(option);
                    }

                    var update = document.createElement("button");
                        update.id = info[i]['flight_num'];
                        update.innerHTML = "Update";
                        update.classList.add("update_button");
                        update.type = "submit";
                        status_change_form.appendChild(form_airline_name);
                        status_change_form.appendChild(form_flight_num);
                        status_change_form.appendChild(status);
                        status_change_form.appendChild(update);
                        form_li.appendChild(status_change_form);


                    document.getElementById("result").appendChild(airline_name);
                    document.getElementById("result").appendChild(flight_num);
                    document.getElementById("result").appendChild(depature_ap);
                    document.getElementById("result").appendChild(departure_time);
                    document.getElementById("result").appendChild(arrival_ap);
                    document.getElementById("result").appendChild(arrival_time);
                    document.getElementById("result").appendChild(price);
                    document.getElementById("result").appendChild(form_li);

                }
                */
                location.reload();
            }
        });
        event.preventDefault();
    });
});



