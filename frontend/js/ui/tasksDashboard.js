const tasksDashboard = document.getElementById("tasksDashboard");
const allTasks = document.getElementById("allTasks");
const ongoingTasks = document.getElementById("ongoing");
const completedTasks = document.getElementById("completed");
import { getTasks, getTask, toggleTask, getOngoingTasks, getCompletedTasks } from "../api/tasksApi.js";
import { getTaskList } from "../api/taskListsApi.js";
import { displayTaskDetails } from "./tasksDetails.js";
import { addTaskToDashboard } from "../utils/dom.js";

export const middleModal = () => {
    displayTasksDashboard();
    ongoingTasks.addEventListener("click", displayOngoingTasks);
    ongoingTasks.style.cursor = "pointer";

    completedTasks.addEventListener("click", displayCompletedTasks);
    completedTasks.style.cursor = "pointer";

    allTasks.addEventListener("click", displayAllTasks);
    allTasks.style.cursor = "pointer";
}
const displayTasksDashboard = async() => {
    const allTasks = await getTasks();
    tasksDashboard.innerHTML =  "";
    for (const taskData of Object.values(allTasks)) {
        addTaskToDashboard(tasksDashboard, taskData, displayTaskDetails, toggleTask);
    }
}

export const displayTaskList = async(listName) => {
    const taskList = await getTaskList(listName);
    tasksDashboard.innerHTML =  "";
    for (const taskId of taskList.tasks) {
        const taskData = await getTask(taskId);
        addTaskToDashboard(tasksDashboard, taskData, displayTaskDetails, toggleTask);
    }
}
const displayAllTasks = async() => {
    const allTasks = await getTasks();
    tasksDashboard.innerHTML =  "";
    for (const taskData of Object.values(allTasks)) {
        addTaskToDashboard(tasksDashboard, taskData, displayTaskDetails, toggleTask);
    }
}

const displayOngoingTasks = async() => {
    const allTasks = await getOngoingTasks();
    tasksDashboard.innerHTML =  "";
    for (const taskData of Object.values(allTasks)) {
        addTaskToDashboard(tasksDashboard, taskData, displayTaskDetails, toggleTask);
    }
}

const displayCompletedTasks = async() => {
    const allTasks = await getCompletedTasks();
    tasksDashboard.innerHTML =  "";
    for (const taskData of Object.values(allTasks)) {
        addTaskToDashboard(tasksDashboard, taskData, displayTaskDetails, toggleTask);
    }
}

/*
const addTaskToDash = async (taskData) => {
    const task = document.createElement("li");
    task.classList.add("taskItem");

    const textDiv = document.createElement("div");
    textDiv.classList.add("taskText");
    textDiv.innerText = taskData.name;
    textDiv.addEventListener("click", () => displayTaskDetails(taskData.id));

    const checkDiv = document.createElement("div");
    checkDiv.classList.add("taskCheck");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = Boolean(taskData.completed);
    checkbox.addEventListener("change", () => toggleTask(taskData.id));
    checkDiv.appendChild(checkbox);

    task.appendChild(textDiv);
    task.appendChild(checkDiv);
    tasksDashboard.appendChild(task);
}
*/
/*const addTaskToDash = async (taskData) => {
    const task = document.createElement("li");
    task.id = taskData.id;

    const taskTitle = document.createElement("span");
    taskTitle.classList.add("taskTitle");
    taskTitle.innerHTML = taskData.name;
    taskTitle.style.cursor = "pointer";
    taskTitle.addEventListener("click", () => displayTaskDetails(taskData.id));
    
    const taskCheckbox = document.createElement("input");
    taskCheckbox.type = "checkbox";
    taskCheckbox.checked = Boolean(taskData.completed);
    taskCheckbox.classList.add("taskCheckbox");
    taskCheckbox.addEventListener("change", () => {toggleTask(taskData.id); console.log("Toggle"); console.log(taskData.id);})

    task.appendChild(taskTitle);
    task.appendChild(taskCheckbox);
    tasksDashboard.appendChild(task);
}*/