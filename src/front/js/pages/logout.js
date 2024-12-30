import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/login.css";

const Login = () => {
  const navigate = useNavigate();
  const { store, actions } = useContext(Context);
  const [isShow, setIsShown] = useState(false);
  const [user, setUser] = useState({
    nombre: "",
    email: "",
    contraseña: "",
    password_check: "",
  });