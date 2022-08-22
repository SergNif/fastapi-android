# from fitmodels import Userpage, Fitness, DataPage1, DataPage3, DataPage4, DataPage5, DataPage6, DataPage7, DataPage8, DataPage9, DataPage10


from datetime import datetime, timedelta
from sqlalchemy import MetaData, Table, inspect, select as slct
import sys
import inspect as inspectr
from fastapi import Depends, FastAPI, status, HTTPException
from typing import Optional
from fitmodels import *
from fitmodels_recycl import *
from sqlmodel import Field, Session, SQLModel, create_engine, table, column, select
import json
from fitdatabase import engine
from fitdatabase_recycl import engine as engine_recycl
from sqlmodel.sql.expression import Select, SelectOfScalar
# from alembic import op


SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

inspector = inspect(engine)
inspector_recycl = inspect(engine_recycl)
# print(inspector.get_table_names())
tables = inspector.get_table_names()
tables_recycl = inspector_recycl.get_table_names()
# print(f'{tables=}')
# print(engine.table_names())

# metadata_obj = MetaData()
# metadata_obj.reflect(bind=engine)
# for table in reversed(metadata_obj.sorted_tables):
#     print(table)
# #######someengine.execute(table.delete())

# q = engine.execute('SHOW TABLES')
# gg = q.fetchall()
# print(f'{gg=}')


def get_session():
    with Session(engine) as session:
        yield session


def get_session_recycl():
    with Session(engine_recycl) as session_recycl:
        yield session_recycl


# classes = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules['fitmodels']) if (inspect.isclass(cls_obj) and ('page' in cls_name.lower()) )]
# print(classes)
app = FastAPI()


# db = Session(engine)


@app.post('/new_user', response_model=Userpage, status_code=status.HTTP_201_CREATED)
async def create_an_item(*, session: Session = Depends(get_session), item: Userpage):
    print(item)
    db_item = session.query(Userpage).filter(
        Userpage.email == item.email).first()
    print("yes")
    if db_item is not None:
        print("no")
        raise HTTPException(status_code=400, detail="Userpage already exist")
    new_item = Userpage(
        fullname=item.fullname,
        email=item.email,
        password=item.password,
    )

    # with db as session:
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


@app.put('/edit_user/{item_id}', response_model=Userpage, status_code=status.HTTP_200_OK)
async def update_an_item(*, session: Session = Depends(get_session), item_id: int, item: Userpage):
    print(item)
    item_to_update = session.query(Userpage).filter(
        Userpage.id == item_id).first()
    item_to_update.fullname = item.fullname
    item_to_update.email = item.email
    item_to_update.password = item.password

    # with db as session:
    session.commit()
    session.refresh(item_to_update)
    return item_to_update


@app.delete('/delete_user/{item_id}')
async def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item_to_delete = session.query(Userpage).filter(
        Userpage.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resourse not Found")

    # with db as session:
    session.delete(item_to_delete)
    session.commit()
    return item_to_delete


@app.get('/get_all_users/', status_code=200)
async def get_all_items(*, session: Session = Depends(get_session)):
    # with db as session:
    items = session.query(Userpage).all()
    return items


@app.get('/get_one_user/{item_id}', response_model=Userpage, status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_an_item(*, session: Session = Depends(get_session), item_id: int):
    # with db as session:
    item = session.query(Userpage).filter(Userpage.id == item_id).first()
    return item


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# app.put('/fit_update_edit_user/{user_id}', response_model=Fitness, status_code=status.HTTP_200_OK)


@app.patch('/fit_update_user/{user_id}', response_model=Fitness,  status_code=status.HTTP_201_CREATED)
async def patch_an_itemus(*, session: Session = Depends(get_session), user_id: int, 
                          datapage10: DataPage10,
                          datapage1: DataPage1,
                          datapage3: DataPage3,
                          datapage4: DataPage4,
                          datapage5: DataPage5,
                          datapage6: DataPage6,
                          datapage7: DataPage7,
                          datapage8: DataPage8,
                          datapage9: DataPage9,
                          userpage: Userpage,
                          ):

    print("start")
    classes_v = [a for f, a in locals().items() if 'page' in f]
    name_classes = [f for f, a in locals().items() if 'page' in f]
    name_classes_full = [a.__class__.__name__ for f, a in locals().items() if 'page' in f]
    
    classes = [cls_obj for cls_name, cls_obj in inspectr.getmembers(sys.modules['fitmodels']) if (inspectr.isclass(cls_obj) and ('page' in cls_name.lower()) )]
    classes_name = [cls_name for cls_name, cls_obj in inspectr.getmembers(sys.modules['fitmodels']) if (inspectr.isclass(cls_obj) and ('page' in cls_name.lower()) )]

    # print(f'{name_classes_full=} \n {name_classes=} \n {classes=} \n {classes_name=}')

    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine, views=False)
    reversed(metadata_obj.sorted_tables)
# dir(classes)=['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', 
# '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
# '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__',
#  '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__',
#  '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__',
#  '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend',
#  'index', 'insert', 'pop', 'remove', 'reverse', 'sort'] 

    for i,cll in enumerate(classes):
        with Session(engine) as session:
            db_hero = session.get(cll, user_id)
            # print(f'{db_hero.__class__.__name__=}')
            idx= name_classes_full.index(db_hero.__class__.__name__)
            if not db_hero:
                raise HTTPException(status_code=404, detail="Hero not found")
            hero_data = classes_v[idx].dict(exclude_unset=True)
            # print(f'{db_hero=} \n {classes_v[idx]=} \n {hero_data=}')
            for key, value in hero_data.items():
                setattr(db_hero, key, value)
            
            session.add(db_hero)
            session.commit()
            session.refresh(db_hero)


    # args_class = [p[1] for p in locals().items() if 'page' in p[0]]
    # args_param = [p[0] for p in locals().items() if 'page' in p[0]]

    dct={}
    lst=[]
    d={}
    for k, clas in enumerate(classes):
        user = session.query(clas).filter(clas.id == user_id).first()
        # print(f'{object_as_dict(user)=} \n {clas.__name__=}')
        # d = dict(clas = object_as_dict(user))
        d[clas.__name__.lower()] = object_as_dict(user)
        # print(f'{d=}')
        # dct = {**d, **dct}
        # lst.append(d)
        # print(f'{dir(user)=} { d= }')
    # print(f' {[a for a in tables]=}  ')
    # dctn = dict(zip(classes_v, lst))
    # print(f' {dct=}  ')
    # print(f'{lst=}')

        # print(f'{tbl=} \n { result= } \n {type(tbl.c)} \n {tbl.c} \n {tbl.columns}')

        # break


    return {**{"id": user_id}, **d }  # dict(id = 5)

@app.post('/fit_new_weight_day/{user_id}',  status_code=status.HTTP_201_CREATED)
async def create_new_menu_day(*, session_recycl: Session = Depends(get_session_recycl),
                              recyclpage: RecyclPage,
                              user_id: int,
                              ):
    print(f' {recyclpage=}')


    # with Session(engine_recycl) as session:
    # item_to_update =  session_recycl.select(RecyclPage).where(RecyclPage.id == user_id)      #(RecyclPage, user_id)
    item_to_update = session_recycl.exec(select(RecyclPage).where(RecyclPage.id == user_id).where(RecyclPage.date == recyclpage.date)).first()
    # result = item_to_update.first()

    # hero_data = result.dict(exclude_unset=True)
    print(f' {item_to_update=} ')
    if item_to_update is None:
        item_to_upd = RecyclPage(
        id = recyclpage.id,
        date=recyclpage.date,
        age = recyclpage.age,
        time = recyclpage.time,
        desired_weight = recyclpage.desired_weight,
        height = recyclpage.height,
        weight = recyclpage.weight,
        
        header = recyclpage.header,
        menu = recyclpage.menu,
        )
        print(f' {item_to_upd=} ')
        # item_to_update.fullName = userName.fullName
        # item_to_update.email = userName.email
        # item_to_update.password = userName.password
        # item_to_update.fitness_id = user_id
        
        # with Session(engine_recycl) as session_bb:
        session_recycl.add(item_to_upd)
        session_recycl.commit()
        session_recycl.refresh(item_to_upd)

    if item_to_update is not None:
        print(f' {item_to_update=} ')
        item_to_update.id = recyclpage.id
        item_to_update.age = recyclpage.age
        item_to_update.time = recyclpage.time
        item_to_update.desired_weight = recyclpage.desired_weight
        item_to_update.height = recyclpage.height
        item_to_update.weight = recyclpage.weight
        item_to_update.weight = recyclpage.weight
        item_to_update.header = recyclpage.header
        item_to_update.menu = recyclpage.menu

        session_recycl.add(item_to_update)
        session_recycl.commit()
        session_recycl.refresh(item_to_update)



#     metadata_obj = MetaData()
#     metadata_obj.reflect(bind=engine_recycl)
# #     # for m in property_class:
#     # tbl = [a for a in metadata_obj.sorted_tables]
#     for tbl in reversed(metadata_obj.sorted_tables):
#         # t = table('dataPage3', column('id'))
#         # s = select(t).where(t.c.id == user_id)
#         statement = tbl.select().where(tbl.c.id == user_id).where(tbl.c.date == recyclpage.date)
#         print(f' {tbl.c=} ')
#         # statement = tbl.select().where(tbl.name == 'dataPage3')
#         result = session_recycl.exec(statement).first()
#         print(f' {result=} ')
    print(f' {session_recycl.exec(select(RecyclPage).where(RecyclPage.id == user_id).where(RecyclPage.date == recyclpage.date)).first()=}  ')

    return {**{"id": user_id}}


@app.patch('/fit_update_user_ddd/{user_id}',  status_code=status.HTTP_201_CREATED)
async def patch_an_item(*, session: Session = Depends(get_session), user_id: int):

    print("start")
    # classes = [a for f, a in locals().items() if 'page' in f]
    # name_classes = [f for f, a in locals().items() if 'page' in f]
    # print(f'{classes=} \n {name_classes}   ')

    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
#     # for m in property_class:
    # tbl = [a for a in metadata_obj.sorted_tables]
    for tbl in reversed(metadata_obj.sorted_tables):
        # t = table('dataPage3', column('id'))
        # s = select(t).where(t.c.id == user_id)
        statement = tbl.select().where(tbl.c.id == user_id)
        # statement = tbl.select().where(tbl.name == 'dataPage3')
        result = session.exec(statement).first()
        if "recycl" not in tbl.name:

            for i, cl in enumerate(tbl.c):
                print(f'{i=} {cl.name=} {result[i]=}')


#                 setattr(user, c.key, ddc[c.key])

#         session.add(user)
#         session.commit()
#         session.refresh(user)
#     dct={}
#     lst=[]
#     d={}
#     for k, clas in enumerate(classes):
#         user = session.query(clas).filter(clas.id == user_id).first()
#         # d = dict(classes[k] = object_as_dict(user))
#         d[classes_name[k].lower()] = object_as_dict(user)
#         dct = {**d, **dct}
#         lst.append(d)
#         # print(f'{dir(user)=} { d= }')
#     # print(f' {[a for a in tables]=}  ')
#     # dctn = dict(zip(args_class, lst))
#     # print(f' {dct=}  ')

        # print(f'{tbl=} \n { result= } \n {type(tbl.c)} \n {tbl.c} \n {tbl.columns}')

        # break

    return {**{"id": user_id}}  # dict(id = 5)


# @app.patch('/fit_update_user/{user_id}',  status_code=status.HTTP_201_CREATED)
# async def patch_an_item(*, session: Session = Depends(get_session),
#     datapage10: DataPage10,
#     datapage1: DataPage1,
#     datapage3: DataPage3,
#     datapage4: DataPage4,
#     datapage5: DataPage5,
#     datapage6: DataPage6,
#     datapage7: DataPage7,
#     datapage8: DataPage8,
#     datapage9: DataPage9,
#     # datapage: Userpage,
#     user_id: int
#     ):
#     # print(userpage)
#     print("status")
#     args_class = [p[1] for p in locals().items() if 'page' in p[0]]
#     # args_class.append(Userpage)
#     args_param = [p[0] for p in locals().items() if 'page' in p[0]]
#     args_param.append('userpage')
#     classes = [cls_obj for cls_name, cls_obj in inspectr.getmembers(sys.modules['fitmodels']) if (inspectr.isclass(cls_obj) and ('page' in cls_name.lower()) )]
#     classes_name = [cls_name for cls_name, cls_obj in inspectr.getmembers(sys.modules['fitmodels']) if (inspectr.isclass(cls_obj) and ('page' in cls_name.lower()) )]
#     args_class2 = [a for a in dir(clss for clss in classes)]# if not a.startswith('_') and not callable(getattr(clss, a) for clss in classes) ]


#      # [a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj, a))]
#     sept='\n'

#     print(f'{classes=} {sept} {args_class2=}  {sept} {classes_name=}')


#     for k, clas in enumerate(classes):
#         user = session.query(clas).filter(clas.id == user_id).first()

#         idx = args_param.index(classes_name[k].lower())
#         fgh = [c  for c in args_class[idx]][1:]
#         ddc = dict([(key, value) for key, value in fgh])

#         # print(f' { ddc= } ')
#         for c in inspect(user).mapper.column_attrs:
#             if ('id' not in c.key):
#                 # print(f'{ddc[c.key]=}')
#                 setattr(user, c.key, ddc[c.key])

#         session.add(user)
#         session.commit()
#         session.refresh(user)
#     dct={}
#     lst=[]
#     d={}
#     for k, clas in enumerate(classes):
#         user = session.query(clas).filter(clas.id == user_id).first()
#         # d = dict(classes[k] = object_as_dict(user))
#         d[classes_name[k].lower()] = object_as_dict(user)
#         dct = {**d, **dct}
#         lst.append(d)
#         # print(f'{dir(user)=} { d= }')
#     # print(f' {[a for a in tables]=}  ')
#     # dctn = dict(zip(args_class, lst))
#     # print(f' {dct=}  ')


#     return {**{"id": user_id}, **dct}


@app.post('/fit_new_user/',  status_code=status.HTTP_201_CREATED)
async def create_an_item(*, session: Session = Depends(get_session),
                         datapage10: DataPage10,
                         datapage1: DataPage1,
                         datapage3: DataPage3,
                         datapage4: DataPage4,
                         datapage5: DataPage5,
                         datapage6: DataPage6,
                         datapage7: DataPage7,
                         datapage8: DataPage8,
                         datapage9: DataPage9,
                         userpage: Userpage,
                         # id: str,
                         ):
    # print(userpage)
    db_item = session.query(Userpage).filter(
        Userpage.email == userpage.email).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Userpage already exist")
    args_class = [p[1] for p in locals().items() if 'page' in p[0]]
    args_param = [p[0] for p in locals().items() if 'page' in p[0]]
    print('________________-------------__________')
    # print(f'{args_class=} /n {args_param=}')
    # print(type(args_param[2]))
    # new_item = Userpage()
    result = ""
    property_class = [a for a in dir(Fitness()) if (
        not a.startswith('__') and not a.startswith('_'))]
    new_item = Fitness()
    # for m in property_class:
    #     if(hasattr(new_item, m) and hasattr(userpage, m)):
    #         try:
    #             s = getattr(userpage, m)
    #             setattr(new_item, m, s)
    #         except Exception:
    #             pass
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    id_num = new_item.id
    print(f'{ new_item.id= } { id_num= }')
    # session.close()
    # print(type(new_item))
    # result += new_item
    diction = {}  # dict(new_item)
    for i, dclass in enumerate(args_class):
        property_class = [a for a in dir(dclass) if (
            not a.startswith('__') and not a.startswith('_'))]
        # print(f'{property_class=}')
        new_class = dclass
        dict_dclass = dict(dclass)

        dict_dclass = {args_param[i]: dict(list(dict_dclass.items())[1:])}
        diction = {**diction, **dict_dclass}
        # json_dclass += json.dumps(dict_dclass)
        # print(f'{diction=}')
        setattr(new_class, 'id', id_num)
        setattr(new_class, 'fitness_id', id_num)
        for m in property_class:
            # print('_________----------_________------')
            # print(m)
            if (m == 'id') or (m == 'fitness_id'):
                setattr(new_class, m, id_num)
                print(f'{ new_class.id= } { id_num= }')
            else:
                if i == 0:
                    if(hasattr(new_class, m) and hasattr(datapage10, m)):
                        try:
                            s = getattr(datapage10, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 1:
                    if(hasattr(new_class, m) and hasattr(datapage1, m)):
                        # id_item = session.dataquery(Page1).filter(
                        #                 Page1.id >= 0).all()
                        # ides = result.all()
                        # print(f'{type(id_item)=}  {id_item=}')
                        try:
                            s = getattr(datapage1, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 2:
                    if(hasattr(new_class, m) and hasattr(datapage3, m)):
                        try:
                            s = getattr(datapage3, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 3:
                    if(hasattr(new_class, m) and hasattr(datapage4, m)):
                        try:
                            s = getattr(datapage4, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 4:
                    if(hasattr(new_class, m) and hasattr(datapage5, m)):
                        try:
                            s = getattr(datapage5, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 5:
                    if(hasattr(new_class, m) and hasattr(datapage6, m)):
                        try:
                            s = getattr(datapage6, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 6:
                    if(hasattr(new_class, m) and hasattr(datapage7, m)):
                        try:
                            s = getattr(datapage7, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 7:
                    if(hasattr(new_class, m) and hasattr(datapage8, m)):
                        try:
                            s = getattr(datapage8, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 8:
                    if(hasattr(new_class, m) and hasattr(datapage9, m)):
                        try:
                            s = getattr(datapage9, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
                if i == 9:
                    if(hasattr(new_class, m) and hasattr(userpage, m)):
                        try:
                            s = getattr(userpage, m)
                            setattr(new_class, m, s)
                        except Exception:
                            pass
            new_class.id = id_num
            new_class.fitness_id = id_num
            session.add(new_class)
            session.commit()
            session.refresh(new_class)

    # statement = select(Userpage).where(Userpage.email == userpage.email)
    # result = session.exec(statement).first()
    # dict_result = {'id': result.id}
    # diction = {**diction, **dict(list(new_item)[1:])}
    # diction = {**dict_result, **diction}
    # # print(f'{diction=}')
    # return {**diction}  # new_item # args_class[1]  #result #new_item
    diction = {}
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    for tbl in reversed(metadata_obj.sorted_tables):
        # print(tbl.select().where(tbl.c.id == idQuery))
        statement = tbl.select().where(tbl.c.id == id_num)
        result = session.exec(statement).first()
        # print(f'{tbl.c.items=}  {tbl.c.keys=}')
        # for b in tbl.c:
        #     print(f'{b.name}')
        if "recyc" not in tbl.name:
            v = [b.name for b in tbl.c]
            # print(f'{list(v)=}')
            print(f'{tbl.name=}')
            dctn = dict(zip(v, list(result)))
            dct = {tbl.name: dctn}
            print(f' {dct=}')
            # diction = {**diction, **dict(list(result)[1:])}
            # diction = {**diction, **dict(result)}
            diction = {**diction, **dct}

    # print('--------_____________-------____________')
    # # print(dict(list(result)[1:]))
    # print(f'{diction=}')
    # print('--------_____________-------____________')

    # {{id:idQuery}:diction} #dict(list(result)[1:])
    return {**{"id": id_num}, **diction}





@app.post('/fit_new_menu_day/{position}',  status_code=status.HTTP_201_CREATED)
async def create_new_menu_day(*, session_recycl: Session = Depends(get_session_recycl),
                              recyclpage: RecyclPage,
                              position: int,
                              ):
    print(recyclpage)
    posit = position - 1
    # db_item = session_recycl.query(Userpage).filter(
    #     RecyclPage.id == recyclpage.id).first()
    # if db_item is not None:
    #     raise HTTPException(status_code=400, detail="Userpage already exist")
    if(posit >= 0):

        item_to_update = session_recycl.query(RecyclPage).filter(
            RecyclPage.id_tab == (posit)).first()

        property_class = [a for a in dir(RecyclPage()) if (
            not a.startswith('__') and not a.startswith('_'))]
        # item_to_update = Fitness()
        # for m in property_class:
        #     if(hasattr(item_to_update, m) and hasattr(recyclpage, m)):
        #         try:
        #             s = getattr(recyclpage, m)
        #             setattr(item_to_update, m, s)
        #         except Exception:
        #             pass
        item_to_update.menu = recyclpage.menu
        item_to_update.weight = recyclpage.weight
        item_to_update.header = recyclpage.header

        # with db as session_recycl:
        session_recycl.commit()
        session_recycl.refresh(item_to_update)

    else:
        args_class = [p[1] for p in locals().items() if 'recycl' in p[0]]
        args_param = [p[0] for p in locals().items() if 'recycl' in p[0]]
        print('________________-------------__________')
        print(f'{args_class=} /n {args_param=}')
        # print(type(args_param[2]))
        # new_item = Userpage()
        result = ""
        property_class = [a for a in dir(RecyclPage()) if (
            not a.startswith('__') and not a.startswith('_'))]
        print(f' {property_class=} ')
        new_item = RecyclPage(id=recyclpage.id,
                              age=recyclpage.age, date=recyclpage.date, time=recyclpage.time, desired_weight=recyclpage.desired_weight,
                              height=recyclpage.height, weight=recyclpage.weight, header=recyclpage.header, menu=recyclpage.menu
                              )

        # id_num = new_item.id
        print(f'{new_item.id=}')

        session_recycl.add(new_item)
        session_recycl.commit()
        session_recycl.refresh(new_item)
        print(f' 2 {new_item.id=}')
        # diction = dict(new_item)
        # print(f' { diction= } ')
        # session_recycl.close()
        # print(type(new_item))
        # result += new_item

    if (posit >= 0):
        idd = recyclpage.id_tab
        new_item = item_to_update
    else:
        idd = new_item.id

    diction = {}  # dict(new_item)
    statement = select(RecyclPage).where(RecyclPage.id == idd)  # new_item.id)
    result = session_recycl.exec(statement).first()
    dict_result = {'id': recyclpage.id}  # result.id}
    diction = {**diction, **dict(list(new_item)[1:])}
    diction = {**diction, **dict_result}
    print(f'{diction=}')
    # dict(f=new_item.id)  # new_item # args_class[1]  #result #new_item
    return {**diction}

# @app.post('/fit/', response_model=FitnessRead)
# async def cr_fit(*, session: Session = Depends(get_session), fitn: Fitness):
#         db_fitn = Fitness.from_orm(fitn)
#         session.add(db_fitn)
#         session.commit()
#         session.refresh(db_fitn)
#         return db_fitn

# @app.get('/fitn/{f_id}', response_model=FitnessReadWithDataPage1)
# async def read_ir(*, f_id: int, session: Session = Depends(get_session)):
#     fit = session.get(Fitness, f_id)
#     return fit

# ***********************************************


@app.put('/fit_edit_user/{item_id}', response_model=Fitness, status_code=status.HTTP_200_OK)
async def update_an_item(*, session: Session = Depends(get_session), item_id: int, item: Fitness):
    print(f' { item= } ')
    item_to_update = session.query(Fitness).filter(
        Fitness.id == item_id).first()

    property_class = [a for a in dir(Fitness()) if (
        not a.startswith('__') and not a.startswith('_'))]
    print(f' { property_class= } ')
    # item_to_update = Fitness()
    for m in property_class:
        if(hasattr(item_to_update, m) and hasattr(item, m)):
            try:
                s = getattr(item, m)
                setattr(item_to_update, m, s)
            except Exception:
                pass

    # with db as session:
    session.commit()
    session.refresh(item_to_update)
    return item_to_update


@app.put('/fit_update_edit_user/{user_id}', response_model=Fitness, status_code=status.HTTP_200_OK)
async def update_an_item(*, session: Session = Depends(get_session),

                         datapage10: DataPage10,
                         datapage1: DataPage1,
                         datapage3: DataPage3,
                         datapage4: DataPage4,
                         datapage5: DataPage5,
                         datapage6: DataPage6,
                         datapage7: DataPage7,
                         datapage8: DataPage8,
                         datapage9: DataPage9,
                         userpage: Userpage,
                         user_id: int, item: Fitness):

    classes = [a for f, a in locals().items() if 'page' in f]
    name_classes = [f for f, a in locals().items() if 'page' in f]

    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
#     # for m in property_class:
    # tbl = [a for a in metadata_obj.sorted_tables]
    for tbl in reversed(metadata_obj.sorted_tables):
        t = table('dataPage3', column('id'))
        s = select(t).where(t.c.id == user_id)
        statement = tbl.select().where(tbl.name == 'dataPage3')
        result = session.exec(statement).first()
        print(f' { s= } ')

        break

    return dict(id=5)

# @app.put('/22fit_update_edit_user/{user_id}', response_model=Fitness, status_code=status.HTTP_200_OK)
# async def 22update_an_item(*, session: Session = Depends(get_session),

#                         datapage10: DataPage10,
#                         datapage1: DataPage1,
#                         datapage3: DataPage3,
#                         datapage4: DataPage4,
#                         datapage5: DataPage5,
#                         datapage6: DataPage6,
#                         datapage7: DataPage7,
#                         datapage8: DataPage8,
#                         datapage9: DataPage9,
#                         userpage: Userpage,
#                         user_id: int, item: Fitness):
#     # print(f' { item= } ')
#     # item_to_update = session.query(Fitness).filter(
#     #     Fitness.id == user_id).first()

#     # property_class = [a for a in dir(Fitness()) if ( 'recyc' not in a and
#     #     not a.startswith('__') and not a.startswith('_') and 'page' in a )]
#     # print(f' { property_class= } ')
#     classes = [a for f, a in locals().items() if 'page' in f]
#     name_classes = [f for f, a in locals().items() if 'page' in f]
#     print(f' {classes=}  ')
#     # for vc, b in locals().items():
#     #     print(f' { vc= } { type(vc)= } { b= }')  #<class 'fitmodels.DataPage3'>
#     # for vc in locals().keys():
#     #     print(f' { vc= } { type(vc)= }')
#     #     print(f' { locals[vc]= }') #<class 'fitmodels.DataPage3'>

#     print(f' { type(locals())= } ')
# #     args_class = [p[1] for p in locals().items()][-1]# if ('page' in p[1])]
# #     args_param = [p[0] for p in locals().items()]# if ('recycl' not in p[0] and 'page' in p[0])]
# #     print(f' { args_class= } ')
#     metadata_obj = MetaData()
#     metadata_obj.reflect(bind=engine)
# #     # for m in property_class:
#     # tbl = [a for a in metadata_obj.sorted_tables]
#     for tbl in reversed(metadata_obj.sorted_tables):
#         t = table('dataPage3', column('id'))
#         s = select(t).where(t.c.id == user_id)
#         statement = tbl.select().where(tbl.name == 'dataPage3')
#         result = session.exec(statement).first()
#         print(f' { s= } ')

#         break

#     property_class1 = [a for a in dir(s) if not a.startswith('_') and not a.endswith('_')]
#     # property_class2 = [a for a in dir(classes[i]) if not a.startswith('_')  and not a.endswith('_')]
#     print(f' { property_class1=  }  ')
#         # print(f' { property_class2=  }  ')

#     # for tbl in reversed(metadata_obj.sorted_tables):
#     for i, name_class in enumerate(name_classes):
#         for tbl in metadata_obj.sorted_tables:
#             if tbl.name == name_class:
#                 g = tbl
#                 break
#         print(f' { g=  } ')
#         property_class1 = [a for a in dir(g) if not a.startswith('_') and not a.endswith('_')]
#         # property_class2 = [a for a in dir(classes[i]) if not a.startswith('_')  and not a.endswith('_')]
#         print(f' { property_class1=  }  ')
#         # print(tbl.select().where(tbl.name == m))
#         # ds = tbl.select().where(tbl.name == name_class).where(tbl.c.id == user_id)
#         # v = [b.name for b in ds.c]
#         # print(f' { ds= } ')
#         # result = session.exec(ds).first()
#         # print(f' { result= } ')
#         # statement = select(classes[i]).where(classes[i].id == user_id)
#         # result = session.exec(statement).first()
#         # print(f' 1 { result= }')
#         # item_to_update = session.query(classes[i]).filter(classes[i].id == user_id).first()
#         # print(f' { item_to_update= } ')
# #         statement = tbl.select().where(tbl.c.id == user_id)
# #         # statement = tbl.select().where(tbl.name==m).where(tbl.c.id == user_id)
# #         result = session.exec(statement).first()
# #         for df in result:
# #             vnf=0
# #             # print(f' { dir(df)= } { tbl.name= } ')
# #             print(f'  { tbl.name= } ')
# #             print(f' { locals()[tbl.name]= } ')
# #             print(f' { statement=  }  ')
# #             # frts = select(tbl).where(tbl.name==tbl.name).where(tbl.c.id == user_id)
# #             # print(f' { frts= } ')
# # #         print(f' 1 { result= } { args_class= }')

# # #         property_class = [a for a in dir(df)]# if ( 'recyc' not in a and not a.startswith('__') and not a.startswith('_') and 'page' in a )]
# # #         print(f' { property_class= } ')
# # #         for n, m in enumerate( property_class):

# # # #     # statement = select(m).where(m.id == user_id)
# # # #     # result = session.exec(statement).first()
# # #             if(hasattr(args_class[n], m)):
# # #                 # and hasattr(item, m)):
# # #                 print(f' {m=} ')
# # #                 try:
# # #                     s = getattr(item, m)
# # #                     setattr(args_class[n], m, s)
# # #                 except Exception:
# # #                     pass
#         # property_class1 = [a for a in dir(ds) if not a.startswith('_') and not a.endswith('_')]
#         # property_class2 = [a for a in dir(classes[i]) if not a.startswith('_')  and not a.endswith('_')]
#         # print(f' { property_class1=  }  ')
#         # print(f' { property_class2=  }  ')

#         # print(f' 11 { result=  }  ')
#         # for m in property_class1:
#         #     # print(f' { classes[i]= }  ')
#         #     # print(f' { result= }  ')
#         #     if(hasattr(result, m) and hasattr(classes[i], m)):
#         #         try:
#         #             s = getattr(classes[i], m)
#         #             setattr(result, m, s)
#         #         except Exception:
#         #             pass

#         #     # try:
#         #     #     s = getattr(locals()[name_class], m)
#         #     #     print(f' { s= } ')
#         #     #     setattr(result, m, s)
#         #     #     print(f' { getattr(result, m)= }  ')
#         #     # except Exception:
#         #         # pass
#         # print(f' 22 { result=  }  ')

# #     # # with db as session:
# #     # session.commit()
# #     # session.refresh(item_to_update)
# #     return item_to_update


@app.delete('/fit_delete_user/{item_id}')
async def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item_to_delete = session.query(Fitness).filter(
        Fitness.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resourse not Found")

    # with db as session:
    session.delete(item_to_delete)
    session.commit()
    return item_to_delete


@app.get('/fit_get_all_users/', status_code=200)
async def get_all_items(*, session: Session = Depends(get_session),):
    # with db as session:
    items = session.query(Fitness).all()
    return items


@app.get('/fit_get_one_user2/{item_id}', response_model=Fitness, status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_an_item(*, session: Session = Depends(get_session), item_id: int, emailQuery: Optional[str] = None, passwQuery: Optional[str] = None):
    # with db as session:
    item = {"item_id": item_id}
    # if emailQuery:
    #     item.update({"emailQuery": emailQuery})
    # if passwQuery:
    #     item.update({"passwQuery": passwQuery})

    print(item)

    itemQuery = session.query(Fitness).filter(Fitness.email == item_id).first()
    print('--------_____________-------____________')
    print(itemQuery)
    return item


#  http://195.234.208.168:8085/fit_get_one_user/?id=26&email=x5c%40x4c.x4c&password=123456
@app.get('/fit_get_one_user/',   status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_an_item(*, session: Session = Depends(get_session), idQuery: int, emailQuery: Optional[str] = None, passwQuery: Optional[str] = None):
    # with db as session:
    # item = {"item_id": item_id}
    item = {}
    if idQuery:
        item.update({"idQuery": idQuery})
    if emailQuery:
        item.update({"emailQuery": emailQuery})
    if passwQuery:
        item.update({"passwQuery": passwQuery})
    print('--------_____________-------____________')
    diction = {}
    print(f'{item=}')
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    for tbl in reversed(metadata_obj.sorted_tables):
        # print(tbl.select().where(tbl.c.id == idQuery))
        statement = tbl.select().where(tbl.c.id == idQuery)
        result = session.exec(statement).first()
        # print(f'{tbl.c.items=}  {tbl.c.keys=}')
        # for b in tbl.c:
        #     print(f'{b.name}')
        if "recyc" not in tbl.name:
            v = [b.name for b in tbl.c]
            # print(f'{list(v)=}')
            print(f'{tbl.name=}')
            dctn = dict(zip(v, list(result)))
            dct = {tbl.name: dctn}
            print(f' {dct=}')
            # diction = {**diction, **dict(list(result)[1:])}
            # diction = {**diction, **dict(result)}
            diction = {**diction, **dct}

    print('--------_____________-------____________')
    # print(dict(list(result)[1:]))
    print(f'{diction=}')
    print('--------_____________-------____________')

    # {{id:idQuery}:diction} #dict(list(result)[1:])
    return {**{"id": idQuery}, **diction}


# http://195.234.208.168:8085/fit_get_menu_string/?userMenuQiery=3&dataMenu=1969-12-31

@app.get('/fit_get_menu_string2/',   status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_one_menu(*, session: Session = Depends(get_session), userMenuQiery: int, dataMenu: str):
    # with db as session:
    # item = {"item_id": item_id}
    dct = []

    items = session.query(Userpage).all()
    # dct={**dct,**items}

    for h in items:
        lc = []
        dc = {}
        l = []

        # print(f'{ {"user":dict(h)}= }')
        # print(f'{ {"menu":str(h)}= }')
        # print(f'{ {"data":datetime.now()}= }')

        # print(f'{ dict(user=dict(h), menu=str(h), data= str(datetime.now()))= }')
        dct.append(dict(user=dict(h), menu=[str(p)
                   for p in h], data=str(datetime.now())))

    return dict(listMenuDay=dct)  # lfl


# http://195.234.208.168:8085/fit_get_menu_string/?userMenuQiery=3&dataMenu=1969-12-31
# http://195.234.208.168:8085/fit_get_menu_string/?userMenuQiery=24&startDataMenu=2022-05-29&endDataMenu=2022-05-30

def sort_by_age(dc):
    return dc['data']


@app.get('/fit_get_menu_string/',   status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_one_menu(*, session_recycl: Session = Depends(get_session_recycl), userMenuQiery: int, startDataMenu: str, endDataMenu: str):

    item_to_delete = session_recycl.query(RecyclPage).filter(
        RecyclPage.id == userMenuQiery).filter(RecyclPage.date >= startDataMenu).filter(RecyclPage.date <= endDataMenu).all()
    dct = []
    print(f' {startDataMenu=} {endDataMenu=}  ')
    for h in item_to_delete:  # .sort(key='time', reverse=True):
        dct.append(dict(id_note=h.id_tab, data=h.date, menu=[
                   h.menu], user=h.header, weight=h.weight))  # str(datetime.now())))
    # print(f' {dct=}  ')
    dct.sort(key=sort_by_age)
    print(f' {dct=}  ')

    return dict(listMenuDay=dct)  # lfl


@app.get('/fit_get_chart_weight/',   status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_one_menu(*, session_recycl: Session = Depends(get_session_recycl), userMenuQiery: int, startDataMenu: str, endDataMenu: str):

    item_to_delete = session_recycl.query(RecyclPage).filter(
        RecyclPage.id == userMenuQiery).filter(RecyclPage.date >= startDataMenu).filter(RecyclPage.date <= endDataMenu).all()
    # RecyclPage.id == userMenuQiery).filter(datetime.fromisoformat(RecyclPage.date) >= datetime.fromisoformat(startDataMenu)).filter(datetime.fromisoformat(RecyclPage.date) <= datetime.fromisoformat(endDataMenu)).all()
    dct = []

    for h in item_to_delete:  # .sort(key='time', reverse=True):
        dct.append(dict(data=h.weight))  # str(datetime.now())))
    # print(f' {dct=}  ')
    dct.sort(key=sort_by_age)
    print(f' {dct=}  ')

    return dict(listMenuDay=dct)  # lfl


@app.patch("/fit_update/{user_id}/",  status_code=status.HTTP_200_OK)
async def update_hero(*, session: Session = Depends(get_session), user_id: int, userData: DataPage3, data: Optional[int] = 12578):
    with Session(engine) as session:
        db_hero = session.get(DataPage3, user_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = userData.dict(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(db_hero, key, value)
            print(f' { db_hero=} {key=} {value=} ')
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        # return db_hero

    statement = select(Userpage).where(Userpage.id == user_id)
    result = session.exec(statement).first()
    print(f' 1 { result= }')
    # dict_result = dict(id= result.id)

    diction = {}
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    for tbl in reversed(metadata_obj.sorted_tables):
        # print(tbl.select().where(tbl.c.id == idQuery))
        statement = tbl.select().where(tbl.c.id == user_id)
        result = session.exec(statement).first()
        # print('--------_____________-------____________')
        # print(f'{tbl.name=}  {tbl.c.keys=}')
        # print('--------_____________-------____________')
        # for b in tbl.c:
        #     print(f'{b.name}')
        # print('--------_____________-------____________')
        if ('recyc' not in tbl.name):
            v = [b.name for b in tbl.c]
            print(f'{list(v)=}')
            print(f'{ result= }')
            dctn = dict(zip(v, list(result)))
            dct = {tbl.name: dctn}
            # print(f'{dct=}')
            # diction = {**diction, **dict(list(result)[1:])}
            # diction = {**diction, **dict(result)}
            diction = {**diction, **dct}
        # print(f'{ diction= }')

    # diction = {**diction, **dict(list(new_item)[1:])}
    # diction = {**diction, **dict_result}
    # print(f'{diction=}')
    return {**{"id": user_id}, **diction}


@app.patch("/fit_update_to_user/{user_id}/", response_model=Userpage, status_code=status.HTTP_202_ACCEPTED)
async def update_to_user(*, session: Session = Depends(get_session), user_id: int, userName: Userpage):

    db_hero = session.get(Userpage, user_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    print('start')
    print(f' { type(Userpage.id)= }')
    # print(f' { item= }')
    statement = select(Userpage).where(Userpage.id == user_id)
    item_to_update = session.exec(statement).first()
    
    print(f' { item_to_update= }')

    with Session(engine) as session:
        item_to_update = session.get(Userpage, user_id)

        item_to_update.fullName = userName.fullName
        item_to_update.email = userName.email
        item_to_update.password = userName.password
        item_to_update.fitness_id = user_id
        
        session.add(item_to_update)
        session.commit()
        session.refresh(item_to_update)


    print(f'{item_to_update=}')

    # # with db as session:
    # session.commit()
    # session.refresh(item_to_update)
    return item_to_update


@app.delete("/fit_delete_one_day_menu/{user_id}/{position}/",  status_code=status.HTTP_200_OK)
async def delete_one_menu_day(*, session_recycl: Session = Depends(get_session_recycl),
                              user_id: int,
                              position: int,
                              ):

    # with Session(engine) as session:
    #     db_hero = session.get(DataPage3, user_id)
    #     if not db_hero:
    #         raise HTTPException(status_code=404, detail="Hero not found")
    #     hero_data = userData.dict(exclude_unset=True)
    #     for key, value in hero_data.items():
    #         setattr(db_hero, key, value)
    #     session.add(db_hero)
    #     session.commit()
    #     session.refresh(db_hero)
    #     # return db_hero

    statement = select(RecyclPage).where(
        RecyclPage.id == user_id).where(RecyclPage.id_tab == position)
    result = session_recycl.exec(statement)
    item = result.one()
    session_recycl.delete(item)
    session_recycl.commit()
    # print(f'{ result= }')
    # dict_result = dict(id= result.id)

    dct = []
    # for h in result:  # .sort(key='time', reverse=True):
    #     dct.append(dict(id_note=h.id_tab, data=h.date, menu=[
    #                h.menu], user=h.header, weight=h.weight))  # str(datetime.now())))
    # print(f' {dct=}  ')

    diction = {}  # dict(new_item)
    statement = select(RecyclPage).where(
        RecyclPage.id == user_id)  # new_item.id)
    result = session_recycl.exec(statement).all()
    for h in result:
        dct.append(dict(id_tab=h.id_tab, id=h.id, age=h.age,
                        time=h.time, desired_weight=h.desired_weight, height=h.height,
                        weight=h.weight, header=h.header, menu=h.menu))

    return dict(listMenuDay=dct)  # lfl

    #  http://195.234.208.168:8085/fit_get_one_user/?id=26&email=x5c%40x4c.x4c&password=123456


@app.get('/fit_get_one_user_email/',   status_code=status.HTTP_200_OK)
# , Authorization: str = Header(None)):
async def get_an_item_email(*, session: Session = Depends(get_session), emailQuery: str, passwQuery: str):
    # with db as session:
    # item = {"item_id": item_id}
    item = {}
    # if idQuery:
    # item.update({"idQuery": idQuery})
    if emailQuery:
        item.update({"emailQuery": emailQuery})
    if passwQuery:
        item.update({"passwQuery": passwQuery})
    print('--------_____________-------____________')
    statement = select(Userpage).where(Userpage.email == emailQuery).where(
        Userpage.passwordFB == passwQuery)
    item_to_update = session.exec(statement).first()
    print(f' 1 { item_to_update= }')

    # print(f' { item_to_update= }')
    # item_to_update.fullName = userName.fullName
    # item_to_update.email = userName.email
    # item_to_update.passwordFB = userName.passwordFB
    # item_to_update.fitness_id = userName.id

    # # # with db as session:
    # session.commit()
    # session.refresh(item_to_update)

    return item_to_update

    # dict_result = {'id': recyclpage.id}  # result.id}
    # diction = {**diction, **dict(list(new_item)[1:])}
    # diction = {**diction, **dict_result}
    # print(f'{diction=}')      fastapi-android

# …or create a new repository on the command line
# echo "# fastapi-android" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/SergNif/fastapi-android.git
# git push -u origin main
# …or push an existing repository from the command line
# git remote add origin https://github.com/SergNif/fastapi-android.git
# git branch -M main
# git push -u origin main


    # return {**{"id": user_id}, **diction}

    # item = {}
    # if idQuery:
    #     item.update({"idQuery": idQuery})
    # if emailQuery:
    #     item.update({"emailQuery": emailQuery})
    # if passwQuery:
    #     item.update({"passwQuery": passwQuery})
    # print('--------_____________-------____________')
    # diction = {}
    # print(f'{item=}')
    # metadata_obj = MetaData()
    # metadata_obj.reflect(bind=engine)
    # for tbl in reversed(metadata_obj.sorted_tables):
    #     # print(tbl.select().where(tbl.c.id == idQuery))
    #     statement = tbl.select().where(tbl.c.id == idQuery)
    #     result = session.exec(statement).first()
    #     # print(f'{tbl.c.items=}  {tbl.c.keys=}')
    #     # for b in tbl.c:
    #     #     print(f'{b.name}')
    #     v = [b.name for b in tbl.c]
    #     # print(f'{list(v)=}')
    #     dctn = dict(zip(v, list(result)))
    #     dct = {tbl.name: dctn}
    #     print(f'{dct=}')
    #     # diction = {**diction, **dict(list(result)[1:])}
    #     # diction = {**diction, **dict(result)}
    #     diction = {**diction, **dct}

    # print('--------_____________-------____________')
    # # print(dict(list(result)[1:]))
    # print(f'{diction=}')
    # print('--------_____________-------____________')

    # return {**{"id": idQuery}, **diction}#{{id:idQuery}:diction} #dict(list(result)[1:])
