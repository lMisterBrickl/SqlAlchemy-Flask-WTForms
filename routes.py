
from webapp.app import app, db
from webapp.models import Carton,Color,Emba,Simca
from webapp.forms import Carton_add_row, Color_add,Search_color, Search_carton, Result_color, Delete_data, Showtable, Result_carton, Delete_carton
from flask import render_template, flash, request, url_for, redirect, flash
from sqlalchemy import and_


@app.route('/')
def index():
    return redirect(url_for('home'))
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form1 = Search_carton()
    form2 = Result_carton()
    form3 = Delete_carton()
    if request.method == 'POST':
        if db.session.query(Carton).filter(and_(Carton.client == form1.search.data, Carton.dimensiune == form1.search1.data)).first() or form2.id_cart.data or form3.nume_cart.data:
            if form1.submit.data and form1.validate_on_submit():
                res = db.session.query(Carton).filter(and_(Carton.client == form1.search.data, Carton.dimensiune == form1.search1.data)).first()
                i = db.session.query(Color).filter(Color.id == res.culoare1_id).first()
                r = db.session.query(Color).filter(Color.id == res.culoare2_id).first()
                form2.id_cart.data = res.id
                form2.client_cart.data = res.client
                form2.oras_cart.data = res.oras
                form2.dimensiune_cart.data = res.dimensiune
                form2.stampila_cart.data = res.stampila
                form2.stanta_cart.data = res.stanta
                form2.notite_cart.data = res.notite
                form3.nume_cart.data = form2.id_cart.data
                if i:
                    form2.cul1_cart.data = i.nume
                if r:
                    form2.cul2_cart.data = r.nume
            if form2.submit1.data:
                res = db.session.query(Carton).filter(Carton.id == form2.id_cart.data).first()
                res.client = form2.client_cart.data
                res.oras = form2.oras_cart.data
                res.dimensiune = form2.dimensiune_cart.data
                res.stampila = form2.stampila_cart.data
                res.stanta = form2.stampila_cart.data
                res.notite = form2.notite_cart.data
                i = db.session.query(Color).filter(Color.nume == form2.cul1_cart.data).first()
                r = db.session.query(Color).filter(Color.id == form2.notite_cart.data).first()
                if i:
                    res.culoare1_id = i.id
                else:
                    emba = Emba(embac = Color(nume = form2.cul1_cart.data),cant1 = 0, cant2 = 0)
                    db.session.add(emba)
                    db.session.commit()
                    simca = Simca(simcac = db.session.query(Color).filter(Color.nume == form2.cul1_cart.data).first(), cant1 =0, cant2= 0)
                    db.session.add(simca)
                    db.session.commit()
                    res.culoare1_id = emba.color_id
                if r:
                    res.culoare2_id = r.id
                    db.session.add(res)
                    db.session.commit()
                else:
                    emba = Emba(embac = Color(nume = form2.cul2_cart.data),cant1 = 0, cant2 = 0)
                    db.session.add(emba)
                    db.session.commit()
                    simca = Simca(simcac = db.session.query(Color).filter(Color.nume == form2.cul2_cart.data).first(), cant1 =0, cant2= 0)
                    db.session.add(simca)
                    db.session.commit()
                    res.culoare2_id = emba.color_id
                    db.session.add(res)
                    db.session.commit()
                flash('Success','success')
            if form3.delete1.data:
                res = db.session.query(Carton).filter(Carton.id == form3.nume_cart.data).first()
                db.session.delete(res)
                db.session.commit()
    return render_template('home.html', form1 = form1, form2 = form2, form3 = form3)

@app.route('/culori', methods = ['GET', 'POST'])
def culori():
    form1 = Search_color()
    form2 = Result_color()
    form3 = Delete_data()
    form4 = Showtable()
    if request.method == 'POST':
        if db.session.query(Color,Emba,Simca).join(Emba).join(Simca).filter(Color.nume == form1.search.data).first() or form2.name1.data or form3.name_cul.data or form4.showtable.data:
            res = db.session.query(Color,Emba,Simca).join(Emba).join(Simca).filter(Color.nume == form1.search.data).first()
            if form1.submit.data and form1.validate_on_submit():
                form2.embacant1.data = res.Emba.cant1
                form2.embacant2.data = res.Emba.cant2
                form2.simcacant1.data = res.Simca.cant1
                form2.simcacant2.data = res.Simca.cant2
                form2.name1.data = res.Emba.color_id
                form3.name_cul.data = res.Color.nume
            if form2.submit1.data:
                i = db.session.query(Emba).filter(Emba.color_id == form2.name1.data).first()
                e = db.session.query(Simca).filter(Simca.color_id == form2.name1.data).first()
                i.cant1 = form2.embacant1.data
                i.cant2 = form2.embacant2.data
                db.session.add(i)
                e.cant1 = form2.simcacant1.data
                e.cant2 = form2.simcacant2.data
                db.session.add(e)
                db.session.commit()
                flash('Success','success')
            if form3.delete.data:
                i = db.session.query(Color).filter(Color.nume == form3.name_cul.data).first()
                e = db.session.query(Emba).filter(Emba.color_id == i.id).first()
                r = db.session.query(Simca).filter(Simca.color_id == i.id).first()
                db.session.delete(i)
                db.session.delete(e)
                db.session.delete(r)
                db.session.commit()
            if form4.showtable.data:
                return redirect(url_for('colortable'))
                
        else: flash('Color does not exist', 'danger')
    return render_template("culori.html", form1 = form1, form2 = form2, form3 = form3, form4 = form4)




@app.route('/addcarton', methods = ['GET', 'POST'])
def addcarton():
    form = Carton_add_row()
    if form.validate_on_submit():

        if form.carton_culoare2.data and not form.carton_culoare1.data:
            flash('Complete Farbe 1 first', 'danger')
        else:         
            if form.carton_culoare2.data:
                if db.session.query(Color).filter(Color.nume == form.carton_culoare1.data).first():
                    if db.session.query(Color).filter(Color.nume == form.carton_culoare2.data).first():
                        cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                            stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                            culoare1 = db.session.query(Color).filter(Color.nume == form.carton_culoare1.data).first(),
                            culoare2 = db.session.query(Color).filter(Color.nume == form.carton_culoare2.data).first())
                    else:
                        cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                            stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                            culoare1 = db.session.query(Color).filter(Color.nume == form.carton_culoare1.data).first(),
                            culoare2 = Color(nume = form.carton_culoare2.data))
                else:
                    if db.session.query(Color).filter(Color.nume == form.carton_culoare2.data).first():
                        cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                            stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                            culoare1 = Color(nume = form.carton_culoare1.data),
                            culoare2 = db.session.query(Color).filter(Color.nume == form.carton_culoare2.data).first())
                    else:
                        cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                            stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                            culoare1 = Color(nume = form.carton_culoare1.data),
                            culoare2 = Color(nume = form.carton_culoare2.data))

            elif form.carton_culoare1.data:
                if db.session.query(Color).filter(Color.nume == form.carton_culoare1.data).first():
                    cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                        stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                        culoare1 = db.session.query(Color).filter(Color.nume == form.carton_culoare1.data).first())
                else:
                    cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                        stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data,
                        culoare1 = Color(nume = form.carton_culoare1.data))
            else: 
                cart = Carton(client = form.carton_name.data, oras = form.carton_oras.data, dimensiune = form.carton_dimens.data,
                         stampila = form.carton_stampila.data, stanta = form.carton_stanta.data, notite = form.carton_notite.data) 

            db.session.add(cart)
            db.session.commit()
            flash('Success!', 'success')
            return redirect(url_for('addcarton'))

    return render_template('addcarton.html', form= form)

@app.route('/addcolor', methods = ['GET', 'POST'])
def addcolor():
    form = Color_add()
    if form.validate_on_submit():
        if not db.session.query(Color).filter(Color.nume == form.color_name.data).first():
            emba = Emba(embac = Color(nume = form.color_name.data),cant1 = 0, cant2 = 0)
            db.session.add(emba)
            db.session.commit()
            simca = Simca(simcac = db.session.query(Color).filter(Color.nume == form.color_name.data).first(), cant1 =0, cant2= 0)
            db.session.add(simca)
            db.session.commit()
        else: flash("Color allready exist", "danger")
        return redirect(url_for('addcolor'))
    return render_template('addcolor.html', form = form)

@app.route('/colortable', methods = ['GET'])
def colortable():
    i = db.session.query(Color,Simca,Emba).join(Simca).join(Emba).all()
    return render_template('colortable.html', i=i)
       