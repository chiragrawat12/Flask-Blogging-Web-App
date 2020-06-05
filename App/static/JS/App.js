var updateBtn=document.querySelector(".updateInfoBtn");
try{
    updateBtn.addEventListener("click",function(){
        var updateBtn=document.querySelector(".updateInfoBtn");
        var update=document.querySelector(".updateForm");
        if(update.style.display==="none"){
            update.style.display="block";
            updateBtn.style.display="none";
        }
        else{
            update.style.display="none";
        }
    })
}
catch(err){
    console.log(err)
}

var closeBtn=document.querySelector(".close");

try{
    closeBtn.addEventListener("click",function(){
        var update=document.querySelector(".updateForm");
        var updateBtn=document.querySelector(".updateInfoBtn");
        if(update.style.display==="block" && updateBtn.style.display==="none"){
            update.style.display="none";
            updateBtn.style.display="block"
        }
    });
}
catch(err){
    console.log(err)
}

var Choose_File=document.getElementById("SelectPP");
try{
    Choose_File.addEventListener("change",function(){
        var dis = document.querySelector(".Choose-File");
        if(Choose_File.options[Choose_File.selectedIndex].value ==="choose-file"){
            if(dis.style.display==="none"){
                dis.style.display="block";
            }
        }
        else if(Choose_File.options[Choose_File.selectedIndex].value === "remove-profile" || Choose_File.options[Choose_File.selectedIndex].value === "do-nothing"){
                dis.style.display="none";
        }
    
    });
}catch(err){
    console.log(err)
}

var del= document.getElementById("delete_btn");
try{
    del.addEventListener("click",function(){
        var conf = document.querySelector(".confirm")
        var edit = document.querySelector("#edit_btn")
        if(conf.style.display == "none"){
                conf.style.display = "block" 
                edit.style.display = "none"
        }
        else{
            edit.style.display = "inline-block"
            conf.style.display = "none"
        }
    })
}
catch(err){
    console.log(err)
}
