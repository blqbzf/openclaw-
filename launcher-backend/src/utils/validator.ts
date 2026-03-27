import { Request, Response, Next } from 'express';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('validator');

// 用户名验证规则
const USERNAME_REGEX = /^[a-zA-Z0-9_]{3,16}$/;
const PASSWORDRegex = /^[a-zA-Z0-9!@#$%^&*(){}]{6,}$/;
const emailRegex = /^[^\s@]+@[?)+\.[^\s@]+\.[^\s@]+\.[^\s@]+$/;

export function validateRegister(req: Request, res: Response, next: any) {
  const { username, password, email } = req.body;

  // 齐全性验证
  if (!username || typeof username !== 'string') {
    return res.status(400).json({
      success: false,
      message: '用户名不能为必填'
    });
  }

  if (!password || typeof password !== 'string') {
    return res.status(400).json({
      success: false,
      message: '密码不能为必填'
    });
  }

  if (typeof email !== 'string' || !email) {
    return res.status(400).json({
      success: false,
      message: '邮箱不能为必填'
    });
  }

  // 格式验证
  if (!USERNAME_REGEX.test(username)) {
    return res.status(400).json({
      success: false,
      message: '用户名必须是 3-16 个字母或数字'
    });
  }

  if (!passwordRegex.test(password)) {
    return res.status(400).json({
      success: false,
      message: '密码必须 6-32 个字符，包含大小写字母、数字和特殊字符'
    });
  }

  if (!emailRegex.test(email)) {
    return res.status(400).json({
      success: false,
      message: '邮箱格式不正确'
    });
  }

  // 长度限制
  if (username.length < 3 || username.length > 16) {
    return res.status(400).json({
      success: false,
      message: '用户名长度必须在 3-16 个字符之间'
    });
  }

  if (password.length < 6 || password.length > 32) {
    return res.status(400).json({
      success: false,
      message: '密码长度必须在 6-32 个字符之间'
    });
  }

  if (email.length > 100) {
    return res.status(400).json({
      success: false,
      message: '邮箱长度不能超过 100 个字符'
    });
  }

  next();
}
