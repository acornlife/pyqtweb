src = """

(function() {
    var initialX = 0;
    var initialY = 0;

    function onMouseMove(ev) {
        var x = ev.screenX - initialX;
        var y = ev.screenY - initialY;
        var args = {0: x, 1: y};
        window.pyqtweb._QWebchannel.objects._bridge.Invoke('WindowMove',JSON.stringify(args) ,'move');
    }

    function onMouseUp() {
        window.removeEventListener('mousemove', onMouseMove);
        window.removeEventListener('mouseup', onMouseUp);
    }

    function onMouseDown(ev) {
        initialX = ev.clientX;
        initialY = ev.clientY;
        window.addEventListener('mouseup', onMouseUp);
        window.addEventListener('mousemove', onMouseMove);
    }
    
    window.addEventListener("load", (event) => {
        var dragBlocks = document.querySelectorAll('%(drag_selector)s');
        for (var i=0; i < dragBlocks.length; i++) {
            dragBlocks[i].addEventListener('mousedown', onMouseDown);
        }
    });
    
})();

"""
