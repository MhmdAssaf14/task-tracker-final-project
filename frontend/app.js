const API_BASE_URL = 'http://localhost:8000';
const STATUSES = ['to_do', 'in_progress', 'done'];
const STATUS_LABELS = {
  to_do: 'To do',
  in_progress: 'In progress',
  done: 'Done',
};

let tasks = [];
let editingOriginalTask = null;

const elements = {
  error: document.querySelector('#error-message'),
  modal: document.querySelector('#task-modal'),
  form: document.querySelector('#task-form'),
  modalTitle: document.querySelector('#modal-title'),
  newTaskButton: document.querySelector('#new-task-button'),
  closeModalButton: document.querySelector('#close-modal-button'),
  cancelButton: document.querySelector('#cancel-button'),
  deleteButton: document.querySelector('#delete-task-button'),
  taskId: document.querySelector('#task-id'),
  title: document.querySelector('#task-title'),
  description: document.querySelector('#task-description'),
  status: document.querySelector('#task-status'),
  priority: document.querySelector('#task-priority'),
  assignee: document.querySelector('#task-assignee'),
  dueDate: document.querySelector('#task-due-date'),
  tags: document.querySelector('#task-tags'),
  statusFilter: document.querySelector('#status-filter'),
  priorityFilter: document.querySelector('#priority-filter'),
  tagFilter: document.querySelector('#tag-filter'),
  overdueFilter: document.querySelector('#overdue-filter'),
  clearFiltersButton: document.querySelector('#clear-filters-button'),
};

function showError(message) {
  elements.error.textContent = message;
  elements.error.hidden = false;
}

function clearError() {
  elements.error.textContent = '';
  elements.error.hidden = true;
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    let detail = `Request failed with HTTP ${response.status}`;
    try {
      const body = await response.json();
      detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
    } catch {
      // Keep the default detail when the response does not contain JSON.
    }
    throw new Error(detail);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function filterQueryString() {
  const params = new URLSearchParams();
  if (elements.statusFilter.value) params.set('status', elements.statusFilter.value);
  if (elements.priorityFilter.value) params.set('priority', elements.priorityFilter.value);
  if (elements.tagFilter.value.trim()) params.set('tag', elements.tagFilter.value.trim());
  if (elements.overdueFilter.checked) params.set('overdue', 'true');
  const query = params.toString();
  return query ? `?${query}` : '';
}

async function loadTasks() {
  clearError();
  try {
    tasks = await apiRequest(`/tasks${filterQueryString()}`);
    renderBoard();
  } catch (error) {
    showError(error.message);
  }
}

function renderBoard() {
  STATUSES.forEach((status) => {
    const list = document.querySelector(`#column-${status}`);
    const count = document.querySelector(`#count-${status}`);
    const statusTasks = tasks.filter((task) => task.status === status);

    list.innerHTML = '';
    count.textContent = statusTasks.length;

    if (statusTasks.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = 'No tasks here';
      list.appendChild(empty);
      return;
    }

    statusTasks.forEach((task) => list.appendChild(createTaskCard(task)));
  });
}

function createTaskCard(task) {
  const card = document.createElement('article');
  card.className = 'task-card';
  card.draggable = true;
  card.dataset.taskId = task.id;

  const tags = task.tags
    .map((tag) => `<span class="tag-chip">${escapeHtml(tag)}</span>`)
    .join('');

  const dueDate = task.due_date
    ? `<span class="pill ${task.is_overdue ? 'overdue' : ''}">${task.is_overdue ? 'Overdue' : 'Due'} ${task.due_date}</span>`
    : '';

  card.innerHTML = `
    <div class="card-title">
      <h3>${escapeHtml(task.title)}</h3>
      <span class="pill ${task.priority}">${escapeHtml(task.priority)}</span>
    </div>
    ${task.description ? `<p>${escapeHtml(task.description)}</p>` : ''}
    <div class="card-meta">
      <span class="pill">${STATUS_LABELS[task.status]}</span>
      ${task.assignee ? `<span class="pill">${escapeHtml(task.assignee)}</span>` : ''}
      ${dueDate}
    </div>
    ${tags ? `<div class="tag-list">${tags}</div>` : ''}
  `;

  card.addEventListener('click', () => openEditModal(task));
  card.addEventListener('dragstart', (event) => {
    event.dataTransfer.setData('text/plain', String(task.id));
  });

  return card;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => {
    const entities = { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#039;', '"': '&quot;' };
    return entities[character];
  });
}

function parseTags(value) {
  return value
    .split(',')
    .map((tag) => tag.trim())
    .filter(Boolean);
}

function taskFormData() {
  return {
    title: elements.title.value.trim(),
    description: elements.description.value.trim(),
    status: elements.status.value,
    priority: elements.priority.value,
    assignee: elements.assignee.value.trim(),
    due_date: elements.dueDate.value || null,
    tags: parseTags(elements.tags.value),
  };
}

function buildUpdatePayload(original, next) {
  const payload = {};
  ['title', 'description', 'status', 'priority', 'assignee', 'due_date'].forEach((field) => {
    if ((original[field] || null) !== (next[field] || null)) {
      payload[field] = next[field];
    }
  });

  if (JSON.stringify(original.tags || []) !== JSON.stringify(next.tags || [])) {
    payload.tags = next.tags;
  }

  return payload;
}

function openCreateModal() {
  editingOriginalTask = null;
  elements.modalTitle.textContent = 'New task';
  elements.deleteButton.hidden = true;
  elements.taskId.value = '';
  elements.title.value = '';
  elements.description.value = '';
  elements.status.value = 'to_do';
  elements.priority.value = 'medium';
  elements.assignee.value = '';
  elements.dueDate.value = '';
  elements.tags.value = '';
  elements.modal.showModal();
  elements.title.focus();
}

function openEditModal(task) {
  editingOriginalTask = task;
  elements.modalTitle.textContent = 'Edit task';
  elements.deleteButton.hidden = false;
  elements.taskId.value = task.id;
  elements.title.value = task.title;
  elements.description.value = task.description || '';
  elements.status.value = task.status;
  elements.priority.value = task.priority;
  elements.assignee.value = task.assignee || '';
  elements.dueDate.value = task.due_date || '';
  elements.tags.value = (task.tags || []).join(', ');
  elements.modal.showModal();
  elements.title.focus();
}

function closeModal() {
  elements.modal.close();
  editingOriginalTask = null;
}

async function handleSubmit(event) {
  event.preventDefault();
  clearError();

  const payload = taskFormData();
  if (!payload.title) {
    showError('Title is required.');
    return;
  }

  try {
    if (editingOriginalTask) {
      const updatePayload = buildUpdatePayload(editingOriginalTask, payload);
      if (Object.keys(updatePayload).length > 0) {
        await apiRequest(`/tasks/${editingOriginalTask.id}`, {
          method: 'PATCH',
          body: JSON.stringify(updatePayload),
        });
      }
    } else {
      await apiRequest('/tasks', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
    }
    closeModal();
    await loadTasks();
  } catch (error) {
    showError(error.message);
  }
}

async function deleteCurrentTask() {
  if (!editingOriginalTask) return;
  clearError();
  try {
    await apiRequest(`/tasks/${editingOriginalTask.id}`, { method: 'DELETE' });
    closeModal();
    await loadTasks();
  } catch (error) {
    showError(error.message);
  }
}

function setupDragAndDrop() {
  document.querySelectorAll('.task-list').forEach((list) => {
    list.addEventListener('dragover', (event) => {
      event.preventDefault();
      list.classList.add('drag-over');
    });

    list.addEventListener('dragleave', () => list.classList.remove('drag-over'));

    list.addEventListener('drop', async (event) => {
      event.preventDefault();
      list.classList.remove('drag-over');
      const taskId = Number(event.dataTransfer.getData('text/plain'));
      const nextStatus = list.dataset.status;
      const task = tasks.find((item) => item.id === taskId);
      if (!task || task.status === nextStatus) return;

      const previousTasks = [...tasks];
      task.status = nextStatus;
      renderBoard();

      try {
        await apiRequest(`/tasks/${taskId}`, {
          method: 'PATCH',
          body: JSON.stringify({ status: nextStatus }),
        });
        await loadTasks();
      } catch (error) {
        tasks = previousTasks;
        renderBoard();
        showError(error.message);
      }
    });
  });
}

function setupEvents() {
  elements.newTaskButton.addEventListener('click', openCreateModal);
  elements.closeModalButton.addEventListener('click', closeModal);
  elements.cancelButton.addEventListener('click', closeModal);
  elements.form.addEventListener('submit', handleSubmit);
  elements.deleteButton.addEventListener('click', deleteCurrentTask);

  [elements.statusFilter, elements.priorityFilter, elements.overdueFilter].forEach((element) => {
    element.addEventListener('change', loadTasks);
  });
  elements.tagFilter.addEventListener('input', debounce(loadTasks, 250));
  elements.clearFiltersButton.addEventListener('click', () => {
    elements.statusFilter.value = '';
    elements.priorityFilter.value = '';
    elements.tagFilter.value = '';
    elements.overdueFilter.checked = false;
    loadTasks();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && elements.modal.open) {
      closeModal();
    }
  });
}

function debounce(callback, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => callback(...args), delay);
  };
}

setupEvents();
setupDragAndDrop();
loadTasks();
