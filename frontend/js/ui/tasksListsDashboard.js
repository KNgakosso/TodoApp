const listsDashboard = document.getElementById("listsDashboard");
const createListForm = document.getElementById("createListForm");
const createListButton = document.getElementById("createListButton");
const closeCreateListButton = document.getElementById("closeCreateListButton");
console.log(createListButton);
import { getTaskLists, createTaskList } from "../api/taskListsApi.js";
import { displayTaskList } from "./tasksDashboard.js";

export const leftModal = () => {
    initTaskListsDashboard();
    initcreateTaskListButton();
    createListForm.addEventListener("submit", vaildateCreateListForm);
    closeCreateListButton.addEventListener("click", hideListCreationForm);

}
export const initTaskListsDashboard = async () => {
    const allTaskListsDatas = await getTaskLists()
    listsDashboard.innerHTML=  "";
    for (const taskListData of Object.values(allTaskListsDatas)) {
        const taskList = document.createElement("li");
        taskList.textContent = taskListData.name;
        taskList.style.cursor = "pointer";
        taskList.addEventListener("click", () => {displayTaskList(taskListData.name);});
        listsDashboard.appendChild(taskList);
    }
}

const initcreateTaskListButton = () => {
    createListButton.addEventListener("click", displayListCreationForm);
    createListButton.style.cursor = "pointer";
}

const displayListCreationForm = () => {
    createListForm.hidden = false;
}

const hideListCreationForm = () => {
    createListForm.reset();
    createListForm.hidden = true;
}

const vaildateCreateListForm = async (e) => {
    e.preventDefault();
    const taskListData = {
        name: createListForm.elements.listName.value
    }
    createTaskList(taskListData);
    createListForm.elements.listName.value = "";
    await initTaskListsDashboard();
}