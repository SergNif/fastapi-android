# from fitmodels import Userpage, Fitness, DataPage1, DataPage3, DataPage4, DataPage5, DataPage6, DataPage7, DataPage8, DataPage9, DataPage10


from datetime import datetime, timedelta
from sqlalchemy import MetaData, inspect, select as slct
import sys  # inspect, sys
from fastapi import Depends, FastAPI, status, HTTPException
from typing import Optional
from fitmodels import *
from fitmodels_recycl import *
from sqlmodel import Field, Session, SQLModel, create_engine, select, column
import json
from fitdatabase import engine
from fitdatabase_recycl import engine as engine_recycl
from sqlmodel.sql.expression import Select, SelectOfScalar

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


@app.patch('/fit_update_user/{user_id}',  status_code=status.HTTP_201_CREATED)
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
                         user_id: str,
                         ):
    print(userpage)
    db_item = session.query(Fitness).filter(
        Fitness.id == user_id).first()
    # if db_item is not None:
    #     raise HTTPException(status_code=400, detail="Userpage already exist")
    args_class = [p[1] for p in locals().items() if 'page' in p[0]]
    args_param = [p[0] for p in locals().items() if 'page' in p[0]]
    print('________________-------------__________')
    print(f'{args_class=} /n {args_param=}')
    # print(type(args_param[2]))
    # new_item = Userpage()
    result = ""
    # property_class = [a for a in dir(Fitness()) if (
    #     not a.startswith('__') and not a.startswith('_'))]
    # new_item = Fitness()
    # # for m in property_class:
    # #     if(hasattr(new_item, m) and hasattr(userpage, m)):
    # #         try:
    # #             s = getattr(userpage, m)
    # #             setattr(new_item, m, s)
    # #         except Exception:
    # #             pass
    # session.add(new_item)
    # session.commit()
    # session.refresh(new_item)
    id_num = user_id #new_item.id
    # print(f'{ new_item.id= } { id_num= }')
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
            # session.add(new_class)
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
