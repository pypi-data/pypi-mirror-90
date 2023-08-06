(function() {
    'use strict'

    var symbols = [
        { char: 'F', symbol: '∀' },
        { char: 'X', symbol: '∃' },
        { char: 'S', symbol: '√' },
        { char: '1', symbol: '²' },
        { char: '3', symbol: '∈' },
        { char: '4', symbol: '∉' },
        { char: 'V', symbol: '∨' },
        { char: 'A', symbol: '∧' },
        { char: 'L', symbol: '¬' },
        { char: 'M', symbol: '⇒' },
        { char: 'O', symbol: '⇔' },
        { char: '0', symbol: 'Ø' },
        { char: 'U', symbol: '⊆' },
        { char: 'U', symbol: '∪' },
        { char: 'T', symbol: '∩' },
        { char: 'N', symbol: 'ℕ' },
        { char: 'Z', symbol: 'ℤ' },
        { char: 'Q', symbol: 'ℚ' },
        { char: 'R', symbol: 'ℝ' },
        { char: 'C', symbol: 'ℂ' },
        { char: 'H', symbol: '✔' },
        { char: 'B', symbol: '▣' },
    ];

    var createSymbolElement = function(symbol, char) {
        var symElem = document.createElement('div');
        symElem.classList.add('symbol-value');
        symElem.innerText = symbol;

        var charElem = document.createElement('div');
        charElem.classList.add('symbol-code');
        charElem.innerText = 'Alt+' + char;

        var elem = document.createElement('div');
        elem.classList.add('symbol');
        elem.appendChild(symElem);
        elem.appendChild(charElem);
        return elem;
    };

    var http = function(method, url, data) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open(method, url);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function(evt) {
                if (this.status >= 200 && this.status < 300) {
                    resolve(this.response);
                } else {
                    reject(evt);
                }
            };
            xhr.onerror = reject;
            xhr.send(JSON.stringify(data));
        });
    };

    window.addEventListener('load', function() {
        var title = document.getElementById('title');
        var text = document.getElementById('text');
        var panel = document.getElementById('panel');
        var addBtn = document.getElementById('add-btn');
        var newListing = document.getElementById('new-listing');
        var newTitle = document.getElementById('new-title');

        if (text) {
            var save = (function() {
                var timer = null;
                var status = document.getElementById('status');
                return function() {
                    status.textContent = '';
                    if (timer !== null) {
                        clearTimeout(timer);
                        timer = null;
                    }
                    timer = setTimeout(function() {
                        http('PUT', '', {
                            title: title.value,
                            text: text.value,
                        }).then(function(e) {
                            status.textContent = '✔ Saved';
                        }, function(e) {
                            console.error(e);
                            status.textContent = '✗ Error saving.';
                        });
                    }, 500);
                };
            })();

            var insertText = function(str) {
                var startPos = text.selectionStart;
                var endPos = text.selectionEnd;
                text.value = text.value.substring(0, startPos) + str +
                    text.value.substring(endPos);
                text.selectionStart = text.selectionEnd = startPos + str.length;
                text.focus();
                save();
            };

            var updateRows = function() {
                text.setAttribute('rows', text.value.split("\n").length + 1 || 2);
            };
            updateRows();

            text.addEventListener('input', function() {
                updateRows();
                save();
            });

            text.addEventListener('keydown', function(evt) {
                if (evt.keyCode == 9) {
                    evt.preventDefault();
                    insertText("\t");
                } else if (evt.altKey) {
                    symbols.forEach(function(symbol) {
                        if (evt.keyCode == symbol.char.charCodeAt(0)) {
                            evt.preventDefault();
                            insertText(symbol.symbol);
                        }
                    });
                }
            });

            title.addEventListener('input', function() {
                save();
            });

            symbols.forEach(function(symbol) {
                var elem = createSymbolElement(symbol.symbol, symbol.char);
                elem.addEventListener('click', function() {
                    insertText(symbol.symbol);
                });
                panel.appendChild(elem);
            });
        }

        if (addBtn) {
            addBtn.addEventListener('click', function() {
                newListing.classList.remove('hidden');
                newTitle.focus();
            });

            newTitle.addEventListener('keydown', function(evt) {
                if (evt.keyCode == 27) {
                    newTitle.blur();
                    newTitle.value = '';
                    newListing.classList.add('hidden');
                }
            });
        }
    });
})();