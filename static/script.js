class Form {
    constructor() {
        this.form = 'form:not(.hidden)'
        this.formEl = document.querySelector('.complex-form')
        this.data = {}
        this.cars = null
        this.inputSubmit = document.querySelector('[type="submit"]')
        this.validField = Array.from(document.querySelectorAll('.complex-form [data-valid]'))
        this.blockForText = $('.main-text')
        this.mainText = 'Заказать самогруз - просто. Введите данные груза в поля. Чем больше данных вы заполните, тем точнее получите цену в калькуляторе.'
    }

    changeForm(e) {
        if (this.validate()) {
            this.inputSubmit.removeAttribute('disabled')
        } else {
            this.inputSubmit.setAttribute('disabled', 'disabled')
        }
        const weight = +this.formEl.querySelector('#weight').value
        if (weight) {
            const match = this.cars.filter(car => car.crane > weight)[0]
            if (match) {
                let minTime = match.minTime
                let userTime = +this.formEl.querySelector('#time').value
                if (userTime && userTime > minTime) {
                    document.querySelectorAll('.pricing')
                    .forEach(pricing =>
                        pricing.innerHTML = `${userTime * match.costHour}р.`)
                    return
                }

                document.querySelectorAll('.pricing')
                    .forEach(pricing =>
                        pricing.innerHTML = `${minTime * match.costHour}р. с учетом минимального времени`)
                    return


            }

        }
    }

    focusInput(e) {
        // console.log(e.target.dataset.input)
    }

    blurInput(e) {
        this.blockForText.html(this.mainText)
    }

    validate() {
        return this.validField.every(field => (field.classList.contains('is-valid')))
    }

    submit(e) {
        e.preventDefault()
        if (!this.validate()) return
        let formEl = e.target.closest('form')
        let inputFields = Array.from(formEl.querySelectorAll('input'))
        const response = {}
        response.additional = formEl.querySelector('textarea').value
        inputFields.map(field => {
            if (field.type === 'submit') {
                return;
            } else if (field.type === 'radio') {
                response[field.dataset.field] = field.value
                return
            }
            response[field.id] = field.value
        })
        $.post('/', response, function (data) {

        })
    }

    init() {
        const that = this
        $.get('/?task=getCars', function (cars) {
            that.cars = JSON.parse(cars)
        })
        $(document).on('input', this.form, (e) => mainForm.changeForm(e))
        $(document).on('focus', this.form, (e) => mainForm.focusInput(e))
        $(document).on('blur', this.form, (e) => mainForm.blurInput(e))
        $(document).on('submit', this.form, (e) => mainForm.submit(e))
    }
}

class Car {
    constructor() {
        this.cars = Array.from(document.querySelectorAll('.card'))
        this.car = null
    }

    calculateSum(target) {
        this.car = target.closest('.card')
        if (this.car) {
            document.querySelectorAll('.pricing')
                .forEach(pricing =>
                    pricing.innerHTML = `${+this.car.dataset.minTime * +this.car.dataset.costHour}р. с учетом минимального времени`)
        }
    }

    validate() {
        const input = this.car.querySelector('input')
        if (input.classList.contains('is-valid')) {
            return true
        }
        input.classList.add('is-invalid')
        return false
    }

    submit(e) {
        e.preventDefault()
        this.car = e.target.closest('.card')
        if (!this.validate()) return
        var response = {
            text: this.car.querySelector('.card-title').textContent,
            phone: this.car.querySelector('input').value
        }
        $.post('/car', response, function (data) {
            console.log(data)
        })
    }

    init() {
        this.cars.map(car => {
            car.addEventListener('click', ({target}) => this.calculateSum(target))
            car.querySelector('a').addEventListener('click', (e) => this.submit(e))
            car.querySelector('input').addEventListener('keyup', (e) => {
                if (e.key === 'Enter') {
                    this.submit(e)
                }
            })
        })
    }
}

let changeFormBtns = document.querySelectorAll('[data-change-form]')
let mainForm = new Form()
let car = new Car()
mainForm.init()
car.init()


function openForm() {
    document.querySelectorAll('.form').forEach(form => form.classList.add('hidden'))
    document.querySelector(this.id).classList.remove('hidden')
}

changeFormBtns.forEach(btn => btn.addEventListener('click', openForm))
jQuery(document).on('input', '[data-valid]', validate)


function validate() {
    var reg = new RegExp(jQuery(this).data('valid'));
    var value = jQuery(this).has('value') || jQuery(this).is('select') ? jQuery(this).val() : jQuery(this).text();
    if (reg.test(value)) {
        jQuery(this).removeClass('is-invalid').addClass('is-valid');
    } else {
        jQuery(this).addClass('is-invalid').removeClass('is-valid');
    }
}

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})

$(document).ready(function () {
    $(":input").inputmask();
});