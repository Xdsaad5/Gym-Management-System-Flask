/*//objects related;
const course = {
    title:"OOP",
    Id:1,
    Teacher:"Sir Fareed.",
    //we can add any function in it.
    enroll()
    {
        return "You are successfully enroll.";
    }
}
console.log(course);
//we can add another data memeber:
course.fee=1000;

for (x in course){
    console.log("The course ",x,":",course[x]);
}*/
//2nd way to make objects is constructor:
/*function Course(title,id,teacher)
{
    this.title=title;
    this.id=id;
    this.teacher=teacher;
    this.enroll=function()
    {
        return "Hello you are successfully login.";
    }
}
course=new Course("Pf",2,"Ahmad Ghazali");
console.log(course.teacher);
console.log(course.enroll());
//we can add delete any data member:
delete course.teacher;
console.log(course);
//we can add function in it later:
course.fee=function(){
    return "your fee has been submitted.";
}
console.log(course);
*/
/*var studentObj={firstName:"Saad ",secondName:"Sultan"};
var studentJson={"firstName":"Saad","secondName":"Sultan"};
console.log(typeof studentObj);
console.log(typeof studentJson);*/
