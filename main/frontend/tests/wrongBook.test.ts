import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import WrongBook from '@/pages/WrongBook.vue'
import { useQuestionStore } from '@/stores/questionStore'

const pushMock = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: pushMock
  })
}))

const questionServiceMock = vi.hoisted(() => ({
  getWrongQuestions: vi.fn(),
  removeWrongQuestion: vi.fn()
}))

vi.mock('@/services/questionService', () => ({
  questionService: questionServiceMock
}))

const baseWrongQuestion = {
  id: 11,
  questionId: 11,
  questionText: 'What does KET stand for?',
  questionImage: undefined,
  optionA: 'A level test',
  optionB: 'Key English Test',
  optionC: 'Knowledge English Test',
  optionD: 'Kids English Try',
  correctAnswer: 'B',
  explanation: 'KET 是 Key English Test 的缩写',
  module: 'vocabulary',
  difficulty: 2,
  wrongCount: 1,
  lastWrongAt: new Date().toISOString()
}

describe('WrongBook interactions', () => {
  beforeEach(() => {
    pushMock.mockReset()
    questionServiceMock.getWrongQuestions.mockReset()
    questionServiceMock.removeWrongQuestion.mockReset()
  })

  async function mountComponent(items = [baseWrongQuestion]) {
    const pinia = createPinia()
    setActivePinia(pinia)
    questionServiceMock.getWrongQuestions.mockResolvedValue({
      items,
      total: items.length,
      page: 1,
      pageSize: 20
    })
    questionServiceMock.removeWrongQuestion.mockResolvedValue(undefined)

    const wrapper = mount(WrongBook, {
      global: {
        plugins: [pinia]
      }
    })

    await flushPromises()
    return { wrapper, pinia }
  }

  it('removes a wrong question through the remove button', async () => {
    const { wrapper } = await mountComponent()
    const items = wrapper.findAll('[data-testid="wrong-question-item"]')
    expect(items).toHaveLength(1)

    await items[0].trigger('click')
    await flushPromises()

    const removeBtn = wrapper.get('[data-testid="remove-btn"]')
    await removeBtn.trigger('click')
    await flushPromises()

    expect(questionServiceMock.removeWrongQuestion).toHaveBeenCalledWith(baseWrongQuestion.id)
    expect(wrapper.findAll('[data-testid="wrong-question-item"]').length).toBe(0)
  })

  it('restores question into the learning flow when practicing again', async () => {
    const { wrapper } = await mountComponent()
    const store = useQuestionStore()
    const items = wrapper.findAll('[data-testid="wrong-question-item"]')
    await items[0].trigger('click')
    await flushPromises()

    const practiceBtn = wrapper.get('[data-testid="practice-btn"]')
    await practiceBtn.trigger('click')

    expect(pushMock).toHaveBeenCalledWith('/learning')
    expect(store.currentQuestion?.id).toBe(baseWrongQuestion.questionId)
    expect(store.currentQuestion?.questionText).toBe(baseWrongQuestion.questionText)
  })
})
