src = """

class Listener {
    /**
     * Creates an instance of Listener.
     * @param {string}   事件名称
     * @param {function} 回调
     * @memberof Listener
     */
    constructor(eventName, callback) {
        this.eventName = eventName;
        this.Callback = (data) => {
            callback.apply(this, [data]);
        };
    }
}

window.pyqtweb = {
    drag:{
        should:false,
        x:0,
        y:0,
    },
    _QWebchannel: {},
    Api: {
        _create_api: function (funcList) {
            for (var i = 0; i < funcList.length; i++) {
                var funcName = funcList[i].func;
                var params = funcList[i].params;

                var funBody = "   var __id = Math.random().toString().substring(2);                                                                         " +
                                    "   var args = JSON.stringify(arguments);                                                                               " +
                                    "   var call_serial_no = '" + funcName + "' + '_' + __id;                                                               " +
                                    "   var promise = new Promise(function (resolve, reject) {                                                              " +
                                    "       window.pyqtweb.Api._callbacks[call_serial_no] = window.pyqtweb.Api._process_return(resolve, reject);            " +
                                    "   });                                                                                                                 " +
                                    "   window.pyqtweb._QWebchannel.objects._bridge.Invoke('" + funcName + "',args,__id);                                   " +
                                    "   return promise; "

                window.pyqtweb.Api[funcName] = new Function(params, funBody);
            }
        },
        _callbacks: {},
        Invoke:function (funcName,id,res) {
            var serial_no = funcName +'_' +id;
            if (window.pyqtweb.Api._callbacks[serial_no]) {
                window.pyqtweb.Api._callbacks[serial_no](res);
                delete window.pyqtweb.Api._callbacks[serial_no];
            }
        },
        _process_return: function (resolve, reject) {
            return function (res) {
                var resObj = JSON.parse(res);
                
                if (resObj.code == 0) {
                    resolve(resObj.data)
                } else {
                    console.error(resObj.method,resObj.message)
                    reject(resObj.message)
                }
            }
        }
    },
    EventBus: {
        _listeners: {},
        register: function (eventName, callback) {

            if (!window.pyqtweb.EventBus._listeners[eventName]) {
                window.pyqtweb.EventBus._listeners[eventName] = []
            }
            const thisListener = new Listener(eventName, callback);
            window.pyqtweb.EventBus._listeners[eventName].push(thisListener);
        },
        unregister: function (eventName) {
            delete window.pyqtweb.EventBus._listeners[eventName]
        },
        notify: function (eventName, data) {
            const listeners = window.pyqtweb.EventBus._listeners
            if (listeners[eventName]) {
                for (let i = 0; i < listeners[eventName].length; i++) {
                    let listener = listeners[eventName][i]
                    listener.Callback(data)
                }

            }
        }
    }
}

"""
