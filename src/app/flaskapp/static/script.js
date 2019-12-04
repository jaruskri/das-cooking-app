$(document).ready(function(){

    function firstCapital(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    //test
    //sessionStorage.setItem('photos', '[{"filename":"1575048415058_40007265_3-borges-olive-oil-extra-light.jpg","estimation":["oil","tomato","vinegar","egg","pork","beer"],"estimationWeights":[0.1831430955557787,0.17522823632011994,0.16893262332921002,0.16511059694997504,0.15804805095607616,0.14953739688884005],"estimationMethod":"random","selection":"oil","selectionMethod":"auto"},{"filename":"1575048415065_dogtilt.jpg","estimation":["water","beer","human","onion","sugar"],"estimationWeights":[0.22484562963838145,0.2088397652285855,0.20547758445871894,0.18049983681141657,0.18033718386289763],"estimationMethod":"random","selection":"water","selectionMethod":"auto"},{"filename":"1575048415070_Export-fresh-apple-fruit-price.jpg","estimation":["oil","egg","dog","wine","garlic","beer","onion","tomato"],"estimationWeights":[0.1327917566081407,0.13225077866594137,0.12839475205936415,0.12648977389132515,0.12589679205193285,0.12387026344274779,0.11820167175495014,0.11210421152559782],"estimationMethod":"random","selection":"oil","selectionMethod":"auto"},{"filename":"1575048415074_microwaved_eggs_delish_recipe.0.jpg","estimation":["vinegar","ammonium sulfate"],"estimationWeights":[0.5362225048910992,0.4637774951089009],"estimationMethod":"random","selection":"vinegar","selectionMethod":"auto"},{"filename":"1575048415098_Peterson-meat.jpg","estimation":["dog","wine","garlic","oil"],"estimationWeights":[0.28694524174704583,0.2701712446555973,0.22181409295852259,0.22106942063883425],"estimationMethod":"random","selection":"dog","selectionMethod":"auto"},{"filename":"1575048415101_Wholemeal-loaf-recipe.jpg","estimation":["egg","onion","dog","wine"],"estimationWeights":[0.26961382199337186,0.2668869346764477,0.2451944119255423,0.2183048314046381],"estimationMethod":"random","selection":"egg","selectionMethod":"auto"}]');

    // upload selected photos
    function upload() {
        console.log('Uploading files');
        var fd = new FormData();
        for (i = 0; i < $('#fileinput')[0].files.length; i++) {
            fd.append('photos', $('#fileinput')[0].files[i]);
        }
        $.ajax({
            url: 'upload',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function(response){
                if (response != 0) {
                    $('#fileinput').val('');
                    r = JSON.parse(response);
                    console.log(r);
                    $.extend(photos, photos, r);
                    displayingredients();
                }
            },
        });
    }
    $("#fileinput").change(upload);
    $("#uploadbtn").click(function(){
        $("#fileinput").click();
    });

    // clear loaded photos
    $("#clearbtn").click(function(){
        console.log('Clearing photos');
        sessionStorage.removeItem('photos');
        photos = [];
        $('#fileinput').val('');
        displayingredients();
    });

    // menu
    $("#mySidebar a").click(function(){
        $("#mySidebar").hide();
    });
    $("#mySidebarOpen").click(function(){
        $("#mySidebar").show();
    });

    // prepare manuall add input
    function fillIngredientsDatalist() {
        console.log('Filling ingredients list');
        var ingredients = JSON.parse(sessionStorage.getItem('ingredients'));
        for (i in ingredients) {
            $("#ingredientslist").append('<option value="'+ingredients[i]+'">');
        }
    }

    // load known ingredients
    if (sessionStorage.getItem('ingredients') == null) {
        $.get( "ingredientslist", function(data) {
            sessionStorage.setItem('ingredients', data);
            fillIngredientsDatalist();
        });
    } else {fillIngredientsDatalist();}

    // change selection manually
    function manualSelection(pid, ingr) {
        console.log("Change selection of " + pid);
        photos[pid].selection = ingr;
        photos[pid].selectionMethod = 'manual';
        displayingredients();
    }

    // display loaded ingredients
    function displayingredients() {
        console.log('Displaying ingredients');
        $("#ingredients").html('');
        for (i = 0; i < photos.length; i++) {
            var element = '<div class="w3-quarter"><div class="w3-card-2 ingredientbox" id="ing'+i+'" pid="'+i+'">';
            if (photos[i].filename != null) {element += '<img src="/uploaded/'+photos[i].filename+'">';}
            if (photos[i].selection == null) {photos[i].selection = photos[i].estimation[0];}
            element += '<h3>'+firstCapital(photos[i].selection)+'</h3>';
            element += '<p>';
            est = [...photos[i].estimation];
            var index = est.indexOf(photos[i].selection);
            if (index !== -1) est.splice(index, 1);
            for (e = 0; e < est.length; e++) {
                t = est[e];
                if (e == 0) t = firstCapital(t);
                else element += ', ';
                element += '<a href="javascript:void(0);" pid='+i+'>'+t+'</a>';
            }
            if (est.length > 0) element += '?';
            element += '</p></div></div>';
            $("#ingredients").append(element);
        }
        $(".ingredientbox a").unbind('click').click(function(){
            manualSelection(parseInt($(this).attr('pid')), $(this).text().toLowerCase());
        });
    }

    // load photos from session and display
    if (sessionStorage.getItem('photos') != null) {
        console.log('Loading photos from session.');
        photos = JSON.parse(sessionStorage.getItem('photos'));
        displayingredients();
    }

    // add manually
    function addManually() {
        console.log('Add manually');
        r = {estimation: [$("#addinput").val()], selection: $("#addinput").val(), estimationMethod: 'none', selectionMethod: 'manual'};
        console.log(r);
        photos[photos.length] = r;
        displayingredients();
        $("#addinput").val('');
    }
    $("#addbtn").click(function(){
        addManually();
    });
    $("#addinput").keyup(function(e){
        if(e.keyCode == 13) {
            addManually();
        }
    });

    // on unload store phoots in session
    $(window).on( "unload", function(){
        console.log('Storing in session');
        sessionStorage.setItem('photos', JSON.stringify(photos));
    });

    // continue
    $("#continuebtn").click(function(){
        s = JSON.stringify(photos);
        sessionStorage.setItem('photos', s);
        $("#continueform input").val(s);
        $("#continueform").submit();
    });

});