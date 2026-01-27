const createTaskButton = document.getElementById("createTaskButton");
const rightModalView = document.getElementById("rightModal");
const closeButton = rightModalView.querySelector("#close");

const taskDetailsView = rightModalView.querySelector("#taskDetailsView");
const modifyTaskButton = taskDetailsView.querySelector("#modifyTaskButton");
const deleteTaskButton = taskDetailsView.querySelector("#deleteTaskButton");

const createTaskView = rightModalView.querySelector("#createTaskView");
const createTaskForm = createTaskView.querySelector("form");

const modifyTaskView = rightModalView.querySelector("#modifyTaskView");
const modifyTaskForm = modifyTaskView.querySelector("form");
const cancelModificationButton = modifyTaskView.querySelector("#cancel");

import { getTask, createTask, deleteTask, updateTask, toggleTask } from "../api/tasksApi.js";
import { addTaskToDashboard, updateTaskInDashboard, removeTaskFromDashboard } from "../utils/dom.js";

export const rightModal = () => {
    closeButton.addEventListener("click", closeRightModal);

    createTaskButton.addEventListener("click", openCreationView);

    createTaskForm.addEventListener("submit", validateCreation);

    modifyTaskButton.addEventListener("click", modifyTaskEvent);
    deleteTaskButton.addEventListener("click", deleteTaskEvent);
    
    modifyTaskForm.addEventListener("submit", validateModification);
    cancelModificationButton.addEventListener("click", cancelModification);
}

const closeRightModal = () => {
    createTaskForm.reset();
    modifyTaskForm.reset();
    hideRightModal();
}

const validateCreation = async (e) => {
    e.preventDefault();
    const listName = createTaskForm.elements.listName.value;
    const body = {
        name: createTaskForm.elements.taskName.value,
        description: createTaskForm.elements.description.value,
        deadline: createTaskForm.elements.deadline.value === "" ? null : createTaskForm.elements.deadline.value,
        priority: createTaskForm.elements.priority.value === "" ? 0 : createTaskForm.elements.priority.value,
        }
    createTaskForm.reset();
    const newTask = await createTask(listName, body);
    addTaskToDashboard(tasksDashboard, newTask, displayTaskDetails, toggleTask);
    displayTaskDetails(newTask.id);
}


const modifyTaskEvent = async (e) => {
    e.preventDefault();
    const taskId = e.currentTarget.dataset.id;

    modifyTaskForm.elements.taskName.value = taskDetailsView.querySelector("#detailName").innerHTML;
    modifyTaskForm.elements.description.value = taskDetailsView.querySelector("#detailDescription").innerHTML;
    modifyTaskForm.elements.deadline.value = taskDetailsView.querySelector("#detailDeadline").innerHTML;
    modifyTaskForm.elements.priority.value = taskDetailsView.querySelector("#detailPriority").innerHTML;

    openModificationView();
    modifyTaskForm.dataset.id=taskId;
    cancelModificationButton.dataset.id = taskId;
}

const validateModification = async (e) => {
    e.preventDefault();
    const taskId = modifyTaskForm.dataset.id
    const body = {
        name: modifyTaskForm.elements.taskName.value,
        description: modifyTaskForm.elements.description.value,
        deadline: modifyTaskForm.elements.deadline.value === "" ? null : modifyTaskForm.elements.deadline.value,
        priority: modifyTaskForm.elements.priority.value === "" ? 0 : modifyTaskForm.elements.priority.value,
        }
    modifyTaskForm.reset();
    const newTask = await updateTask(taskId, body);
    updateTaskInDashboard(taskId, newTask);
    displayTaskDetails(taskId);
}

const cancelModification = (e) => {
    e.preventDefault();
    const taskId = e.currentTarget.dataset.id;
    modifyTaskForm.reset();
    displayTaskDetails(taskId);
}

const deleteTaskEvent = async (e) => {
    e.preventDefault();
    const taskId = e.currentTarget.dataset.id;
    await deleteTask(taskId);
    hideRightModal();
    removeTaskFromDashboard(taskId);
}

export const displayTaskDetails = async (taskId) => {
    openTaskDetailsView();
    const task = await getTask(taskId);
    taskDetailsView.querySelector("#detailName").innerHTML = task.name;
    taskDetailsView.querySelector("#detailDescription").innerHTML = task.description;
    taskDetailsView.querySelector("#detailDeadline").innerHTML = task.deadline;
    taskDetailsView.querySelector("#detailPriority").innerHTML = task.priority;
    taskDetailsView.querySelector("#detailListName").innerHTML = task.list_name;
    taskDetailsView.querySelector("#detailCompleted").innerHTML = task.completed;
    modifyTaskButton.dataset.id = taskId;
    deleteTaskButton.dataset.id = taskId;
}    











const openCreationView = () => {
    rightModalView.hidden = false;
    createTaskView.hidden = false;
    taskDetailsView.hidden = true;
    modifyTaskView.hidden = true;
}

const openTaskDetailsView = () => {
    rightModalView.hidden = false;
    createTaskView.hidden = true;
    taskDetailsView.hidden = false;
    modifyTaskView.hidden = true;
}

const openModificationView = () => {
    rightModalView.hidden = false;
    createTaskView.hidden = true;
    taskDetailsView.hidden = true;
    modifyTaskView.hidden = false;
}


const hideRightModal = () => {
    rightModalView.hidden = true;
    createTaskView.hidden = true;
    taskDetailsView.hidden = true;
    modifyTaskView.hidden = true;
}