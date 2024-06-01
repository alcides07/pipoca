export interface iLogin {
  username: string;
  password: string;
}

export interface iRegister {
  username: string;
  email: string;
  password: string;
  passwordConfirmation: string;
}

export interface iAtivacao {
  message: string;
}
