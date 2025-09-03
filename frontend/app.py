import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://backend:8000"

st.set_page_config(page_title="Gestão de Portfólio", layout="wide")

st.title("📊 Gestão de Portfólio de Investimentos")

# Criação das abas
tab1, tab2, tab3 = st.tabs(["📈 Ativos", "💰 Transações", "Resultados"])

# ----------------- Ativos -----------------
with tab1:
    st.header("Ativos")

    # --- Mostrar ativos ---
    with st.expander("📋 Mostrar Ativos"):
        if st.button("🔄 Atualizar lista"):
            r = requests.get(f"{API_URL}/assets/")
            if r.status_code == 200:
                assets = r.json()
                if assets:
                    df = pd.DataFrame(assets)
                    df = df[["id", "ticker", "name", "type"]]
                    df = df.rename(columns={"id": "ID Ativo", "ticker": "Ticker", "name": "Nome", "type": "Tipo"})
                    st.dataframe(df)
                else:
                    st.info("Nenhum ativo cadastrado.")
            else:
                st.error("Erro ao buscar ativos.")

    # --- Cadastrar ativo ---
    with st.expander("➕ Cadastrar Ativo"):
        with st.form("form_ativo"):
            ticker = st.text_input("Ticker")
            name = st.text_input("Nome")
            type_ = st.selectbox("Tipo", ["STOCK", "ETF", "FII", "CRYPTO"])
            submit = st.form_submit_button("Cadastrar")

            if submit:
                data = {"ticker": ticker, "name": name, "type": type_}
                r = requests.post(f"{API_URL}/assets/", json=data)
                if r.status_code == 200:
                    st.success("Ativo cadastrado com sucesso!")
                else:
                    st.error("Erro ao cadastrar ativo")

    # --- Alterar ativo ---
    with st.expander("✏️ Alterar Ativo"):
        with st.form("form_update_asset"):
            asset_id = st.number_input("ID do ativo", min_value=1, step=1)
            new_name = st.text_input("Novo nome")
            new_ticker = st.text_input("Novo Ticker")
            submit = st.form_submit_button("Alterar")
            if submit:
                data_update = {"name": new_name, "ticker": new_ticker}
                r = requests.patch(f"{API_URL}/assets/{asset_id}", json=data_update)
                if r.status_code == 200:
                    st.success("Ativo alterado com sucesso!")
                else:
                    st.error("Erro ao alterar ativo.")

    # --- Excluir ativo ---
    with st.expander("🗑️ Excluir Ativo"):
        asset_id_delete = st.number_input("ID do ativo para excluir", min_value=1, step=1, key="delete_id")
        if st.button("Excluir"):
            r = requests.delete(f"{API_URL}/assets/{asset_id_delete}")
            if r.status_code == 204:
                st.success("Ativo excluído com sucesso!")
            else:
                st.error("ID do ativo não encontrado")


# ----------------- Transações -----------------
with tab2:
    st.header("Transações")

    # --- Mostrar transações ---
    with st.expander("📋 Mostrar Transações"):
        if st.button("🔄 Atualizar lista", key="refresh_transactions"):
            r = requests.get(f"{API_URL}/transactions/")
            if r.status_code == 200:
                transactions = r.json()
                if transactions:
                    df = pd.DataFrame(transactions)
                    df["asset_ticker"] = df["asset"].apply(lambda x: x["ticker"])
                    df = df.drop(columns=["asset"])
                    df = df[["id", "asset_id", "asset_ticker", "operation", "quantity", "price", "date"]]
                    df = df.rename(columns={"id": "ID transação", 
                                            "asset_id": "ID Ativo", 
                                            "asset_ticker": "Ativo(Ticker)", 
                                            "operation": "Operação", 
                                            "quantity": "Quantidade",
                                            "price": "Preço",
                                            "date": "Data" })
                    st.dataframe(df)
                else:
                    st.info("Nenhuma transação encontrada.")
            else:
                st.error("Erro ao buscar transações.")

    # --- Cadastrar transação ---
    with st.expander("➕ Adicionar Transação"):
        ativos_resp = requests.get(f"{API_URL}/assets/").json()
        ativos_dict = {a["ticker"]: a["id"] for a in ativos_resp} if ativos_resp else {}

        with st.form("form_transaction"):
            ativo = st.selectbox("Ativo", list(ativos_dict.keys()))
            date = st.date_input("Data da transação")
            quantity = st.number_input("Quantidade", min_value=0.0, step=0.01)
            price = st.number_input("Preço por unidade", min_value=0.0, step=0.01)
            operation_type = st.selectbox("Tipo", ["BUY", "SELL"])
            submit = st.form_submit_button("Adicionar")

            if submit:
                data = {
                    "asset_id": ativos_dict[ativo],
                    "date": str(date),
                    "quantity": quantity,
                    "price": price,
                    "operation": operation_type
                }
                r = requests.post(f"{API_URL}/transactions/", json=data)
                if r.status_code == 200:
                    st.success("Transação adicionada com sucesso!")
                else:
                    st.error("Erro ao adicionar transação.")

    # --- Alterar transação ---
    with st.expander("✏️ Alterar Transação"):
        with st.form("form_update_transaction"):
            transaction_id = st.number_input("ID da transação", min_value=1, step=1)
            new_quantity = st.number_input("Nova quantidade", min_value=0.1, step=0.1)
            new_price = st.number_input("Novo preço", min_value=0.0, step=0.01)
            date_new = st.date_input("Data da transação")
            submit = st.form_submit_button("Alterar")

            if submit:
                data_update = {"tx_id": transaction_id,"quantity": new_quantity, "price": new_price, "date": str(date_new)}
                r = requests.patch(f"{API_URL}/transactions/{transaction_id}", json=data_update)
                if r.status_code == 200:
                    st.success("Transação alterada com sucesso!")
                else:
                    st.error("Erro ao alterar transação.")

    # --- Excluir transação ---
    with st.expander("🗑️ Excluir Transação"):
        transaction_id_delete = st.number_input(
            "ID da transação para excluir",
            min_value=1,
            step=1,
            key="delete_transaction_id"
        )
        if st.button("Excluir", key="delete_transaction_btn"):
            r = requests.delete(f"{API_URL}/transactions/{transaction_id_delete}")
            if r.status_code == 204:
                st.success("Transação excluída com sucesso!")
            else:
                st.error("ID da transação não encontrado")

    
with tab3:
    with st.expander("Resumo por Ativo"):
        try:
            r = requests.get(f"{API_URL}/transactions/summary/")
            r.raise_for_status()
            data = r.json()

            if not data:
                st.info("Nenhuma posição encontrada.")
            else:
                df = pd.DataFrame(data)

                # 🔎 filtrar apenas ativos com quantidade > 0
                df = df[df["net_quantity"] > 0]

                if df.empty:
                    st.info("Nenhuma posição em aberto (todas as quantidades zeradas).")
                else:
                    fig = px.bar(
                        df,
                        x="net_quantity",
                        y="ticker",
                        color="ticker",
                        orientation="h",
                        title="Posição líquida por ativo",
                        text="net_quantity"
                    )
                    df = df.rename(columns={"ticker": "Ticker", "name": "Nome", "net_quantity": "Quantidade da Posição", "avg_price": "Preço Médio"})
                    st.dataframe(df)

                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar resumo: {e}")
    
    with st.expander("💰 Lucro Realizado"):
        try:
            r = requests.get(f"{API_URL}/transactions/realized/")
            r.raise_for_status()
            data = r.json()

            if not data:
                st.info("Nenhum lucro realizado ainda.")
            else:
                df = pd.DataFrame(data)
                df = df[df["realized_profit"] != 0]
                df2 = df.rename(columns={"ticker": "Ticker", "realized_profit": "Lucro/Prejuízo Realizado"})
                st.dataframe(df2)

                fig = px.bar(
                    df,
                    x="ticker",
                    y="realized_profit",
                    color="ticker",
                    title="Lucro Realizado por Ativo",
                    text="realized_profit"
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar lucros realizados: {e}")
