var max_minelayer = 5;
var minelayer_count_record = 1;
//zindex will be assign zindex=10
function add_minelayer() {
    //add layer canvas
    var minelayers = document.getElementsByClassName('minelayer');
    if (minelayers.length <= max_minelayer) {
        var canvaseParentNode = document.getElementById('painting-area');
        var minenewcanvas = document.createElement("canvas");
        minenewcanvas.style = "position:absolute;border:0px solid; touch-action: none;z-index: 10;";
        minenewcanvas.style.top = top_key;
        minenewcanvas.style.left = left_key;
        minelayer_count_record = minelayer_count_record + 1;
        minenewcanvas.id = "minelayer" + minelayer_count_record;
        minenewcanvas.height = h;
        minenewcanvas.width = w;
        minenewcanvas.className = "minelayer";
        minenewcanvas.style.transform = scaleKey;
        canvaseParentNode.insertBefore(minenewcanvas, can_active.nextElementSibling);
        //add layer_thumbnail
        var thumbnailsParentNode = document.getElementById('layer_thumbnail');
        var thumbnail_active = document.getElementById(('thumbnail_' + can_active.id.slice(9)));
        var li_add = li_template(thumbnailsParentNode, thumbnail_active, minenewcanvas.id.slice(9));
        change_minelayer_active(li_add);
    }
}

function add_minelayer_existed(delete_canvas_pivot, restore_id) {
    //add layer canvas
    var canvaseParentNode = document.getElementById('painting-area');
    var minenewcanvas = document.createElement("canvas");
    minenewcanvas.style = "position:absolute;border:0px solid; touch-action: none;z-index: 10;";
    minenewcanvas.style.top = top_key;
    minenewcanvas.style.left = left_key;
    minenewcanvas.id = restore_id;
    minenewcanvas.height = h;
    minenewcanvas.width = w;
    minenewcanvas.className = "minelayer";
    minenewcanvas.style.transform = scaleKey;
    canvaseParentNode.insertBefore(minenewcanvas, document.getElementById(delete_canvas_pivot).nextElementSibling);
    //add layer_thumbnail
    var thumbnailsParentNode = document.getElementById('layer_thumbnail');
    console.log(delete_canvas_pivot);
    var thumbnail_active = document.getElementById(('thumbnail_' + delete_canvas_pivot.slice(9)));
    li_template(thumbnailsParentNode, thumbnail_active, minenewcanvas.id.slice(9));
}

function li_template(thumbnailsParentNode, thumbnail_active, minelayer_count_record) {
    var minelayers = document.getElementsByClassName('minelayer');
    li = document.createElement("li");
    li.setAttribute("id", "thumbnail_" + minelayer_count_record);
    li.setAttribute("onclick", "change_minelayer_active(this)");
    button = document.createElement("button");
    button.setAttribute("class", "btn");
    button.style.backgroundColor = "white";
    img = document.createElement("img");
    img.setAttribute("class", "mx-2");
    img.width = 75;
    img.height = 75;
    img.style.backgroundColor = "white";
    button.innerHTML += '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16"><path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/><path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/></svg><span class="visually-hidden">Button</span>';
    li.appendChild(button);
    li.appendChild(img);
    thumbnailsParentNode.insertBefore(li, thumbnail_active);
    return li;
}


function delete_minelayer() {
    if (can_active.previousElementSibling.className == "minelayer") {
        restore[restore.length] = ctx_active.getImageData(0, 0, w, h);
        restore_active[restore_active.length] = can_active.id;
        delete_canvas_pivots[delete_canvas_pivots.length] = can_active.previousElementSibling.id;
        var can_active_new = can_active.previousElementSibling;
        can_active.remove();
        document.getElementById('thumbnail_' + (can_active.id.slice(9))).remove();
        can_active = can_active_new;
        ctx_active = can_active.getContext("2d");
        restore[restore.length] = ctx_active.getImageData(0, 0, w, h);
        restore_active[restore_active.length] = can_active.id;
        document.getElementById('thumbnail_' + (can_active.id.slice(9))).style.backgroundColor = 'rgb(95, 103, 255)';
        updateCanvas();
    }
}

function change_minelayer_opacity() {

}

function change_minelayer_order(pivot) {
    var canvaseParentNode = document.getElementById('painting-area');
    var thumbnailsParentNode = document.getElementById('layer_thumbnail');
    var change_thumbnail = document.getElementById('thumbnail_' + (can_active.id.slice(9)))
    if (pivot == 1 && change_thumbnail.previousElementSibling) {
        canvaseParentNode.insertBefore(can_active, can_active.nextElementSibling.nextElementSibling);
        thumbnailsParentNode.insertBefore(change_thumbnail, change_thumbnail.previousElementSibling);
    }
    if (pivot == -1 && change_thumbnail.nextElementSibling) {
        canvaseParentNode.insertBefore(can_active, can_active.previousElementSibling);
        thumbnailsParentNode.insertBefore(change_thumbnail, change_thumbnail.nextElementSibling.nextElementSibling);
    }
    updateCanvas();
}

function change_minelayer_active(obj) {
    // console.log(obj);
    document.getElementById("thumbnail_" + can_active.id.slice(9)).style.backgroundColor = '';
    var id = 'minelayer' + obj.id.slice(10);
    can_active = document.getElementById(id);//active layer (can be modified) 
    ctx_active = can_active.getContext("2d");
    // console.log(can_active);
    restore[restore.length - 1] = ctx_active.getImageData(0, 0, w, h);
    restore_active[restore_active.length - 1] = can_active.id;
    document.getElementById("thumbnail_" + obj.id.slice(10)).style.backgroundColor = 'rgb(95, 103, 255)';
}

function change_minelayer_display() {

}
//Update canvas algorithm(have to combine in one canvas and send)
//Have to add aria in html for interaction for minelayer(add/delete/opacity/order)
//Thumbnail binding active layer listerner,change thumbnail when canvas change

//Not important but useful:change layer name/save,import duplicate layers/