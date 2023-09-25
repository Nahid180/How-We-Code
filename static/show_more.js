//<button id="showMore">click</button>

window.onload = function () {
    document.getElementById('gsc-i-id1').placeholder = 'Search...';
};

var doms = document.getElementsByClassName('content');
var count = 4;
for (var i = 0; i < 4; i++) {
    doms[i].style.display = "block";
}
function load() {
    remaining = doms.length - count;
    if (remaining <= 4) {
        for (var l = count; l < doms.length; l++) {
            doms[l].style.display = 'block';
        }
    }
    else {
        for (var l = count; l < count + 4; l++) {
            doms[l].style.display = 'block';
        }
    }
    count = count + 4;
    if (count > doms.length) {
        document.getElementById('show').style.display = "none";
    }
    else {
        document.getElementById('show').style.display = "block";
    }
}

