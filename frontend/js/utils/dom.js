export const addTaskToDashboard = (container, taskData, onClickText, onToggleCheckbox) => {
    const task = document.createElement("li");
    task.classList.add("taskItem");
    task.id = taskData.id;

    const textDiv = document.createElement("div");
    textDiv.classList.add("taskText");
    textDiv.innerText = taskData.name;
    textDiv.addEventListener("click", () => onClickText(taskData.id));

    const checkDiv = document.createElement("div");
    checkDiv.classList.add("taskCheck");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = Boolean(taskData.completed);
    checkbox.addEventListener("change", () => onToggleCheckbox(taskData.id));
    checkDiv.appendChild(checkbox);

    task.appendChild(textDiv);
    task.appendChild(checkDiv);
    container.appendChild(task);
};


// js/utils/tasksDom.js
export const updateTaskInDashboard = (taskId, newData) => {
    const li = document.getElementById(taskId);
    if (!li) return;

    const textDiv = li.querySelector(".taskText");
    textDiv.innerText = newData.name;

    const checkbox = li.querySelector("input[type='checkbox']");
    checkbox.checked = Boolean(newData.completed);
};

export const removeTaskFromDashboard = (taskId) => {
    const taskElement = document.getElementById(taskId);
    if (!taskElement) return;

    taskElement.remove();
};
