expand = document.getElementById('iconspan');
text = document.getElementById('text');
var isOpen = 0;
expand.onclick = function open(){
                        if(isOpen){
                            text.style.maxHeight = '3em';
                            isOpen = 0;
                        }else{
                            text.style.maxHeight = 'none';
                            isOpen = 1;
                        }
                    }